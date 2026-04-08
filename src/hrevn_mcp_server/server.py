from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .config import settings
from .tools import TOOL_SPECS
from .tools import ToolRegistry


JSONRPC_VERSION = "2.0"


class McpServer:
    def __init__(self):
        self.registry = ToolRegistry()
        self.initialized = False

    def run(self) -> None:
        while True:
            message = self._read_message()
            if message is None:
                return
            response = self._handle_message(message)
            if response is not None:
                self._write_message(response)

    def _handle_message(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        params = message.get("params") or {}
        request_id = message.get("id")

        if method == "notifications/initialized":
            self.initialized = True
            return None

        if method == "ping":
            return self._result(request_id, {})

        if method == "initialize":
            result = {
                "protocolVersion": "2025-03-26",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": {
                    "name": settings.server_name,
                    "version": settings.server_version,
                },
                "instructions": (
                    "HREVN MCP server exposing baseline diagnostics, profile validation, "
                    "bundle generation, and bundle verification through the live managed API."
                ),
            }
            return self._result(request_id, result)

        if method == "tools/list":
            return self._result(request_id, {"tools": self.registry.list_tools()})

        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            if not name:
                return self._error(request_id, -32602, "Missing tool name")
            try:
                result = self.registry.call_tool(name, arguments)
            except KeyError as exc:
                return self._error(request_id, -32601, str(exc))
            return self._result(request_id, result)

        return self._error(request_id, -32601, f"Method not found: {method}")

    def _result(self, request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
        return {
            "jsonrpc": JSONRPC_VERSION,
            "id": request_id,
            "result": result,
        }

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": JSONRPC_VERSION,
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    def _read_message(self) -> dict[str, Any] | None:
        content_length = 0
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            if line in (b"\r\n", b"\n"):
                break
            decoded = line.decode("utf-8").strip()
            if decoded.lower().startswith("content-length:"):
                content_length = int(decoded.split(":", 1)[1].strip())

        if content_length <= 0:
            return None

        body = sys.stdin.buffer.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def _write_message(self, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8")
        sys.stdout.buffer.write(header)
        sys.stdout.buffer.write(body)
        sys.stdout.buffer.flush()


def _run_self_test() -> int:
    payload = {
        "task_type": "ai_workflow",
        "profile": "eu_readiness_profile",
        "record": {
            "agent_name": "claude_code",
            "summary": "MCP self-test",
        },
    }
    result = ToolRegistry().call_tool("baseline_check", payload)
    print(json.dumps(result, indent=2))
    return 0 if not result.get("isError") else 1


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="HREVN MCP server")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the MCP server version and exit.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run a live baseline_check against the configured HREVN managed API and exit.",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="Print the MCP tool names and exit.",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(settings.server_version)
        return

    if args.list_tools:
        print("\n".join(spec.name for spec in TOOL_SPECS))
        return

    if args.self_test:
        raise SystemExit(_run_self_test())

    McpServer().run()


if __name__ == "__main__":
    main()
