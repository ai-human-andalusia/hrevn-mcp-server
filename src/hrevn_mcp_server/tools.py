from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .client import HrevnApiError, HrevnManagedClient


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler_name: str


def _baseline_check_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "task_type": {"type": "string"},
            "profile": {"type": "string"},
            "record": {"type": "object"},
            "metadata": {"type": "object"},
        },
        "additionalProperties": False,
    }


def _profile_validate_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "profile": {"type": "string"},
            "record": {"type": "object"},
            "metadata": {"type": "object"},
        },
        "required": ["profile"],
        "additionalProperties": False,
    }


def _generate_bundle_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "record": {"type": "object"},
            "traces": {
                "type": "array",
                "items": {"type": "object"},
            },
            "options": {
                "type": "object",
                "properties": {
                    "include_report_pdf": {"type": "boolean"}
                },
                "additionalProperties": False,
            },
        },
        "required": ["record"],
        "additionalProperties": False,
    }


def _verify_bundle_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "source": {"type": "string"},
        },
        "required": ["source"],
        "additionalProperties": False,
    }


TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec(
        name="baseline_check",
        description="Run a HREVN baseline diagnostic before a consequential workflow step.",
        input_schema=_baseline_check_schema(),
        handler_name="baseline_check",
    ),
    ToolSpec(
        name="profile_validate",
        description="Validate a HREVN profile payload more deeply once the workflow profile is known.",
        input_schema=_profile_validate_schema(),
        handler_name="profile_validate",
    ),
    ToolSpec(
        name="generate_bundle",
        description="Generate a tamper-evident HREVN evidence bundle from a record and traces.",
        input_schema=_generate_bundle_schema(),
        handler_name="generate_bundle",
    ),
    ToolSpec(
        name="verify_bundle",
        description="Verify a HREVN evidence bundle by source path or bundle artifact path.",
        input_schema=_verify_bundle_schema(),
        handler_name="verify_bundle",
    ),
)


class ToolRegistry:
    def __init__(self, client: HrevnManagedClient | None = None):
        self.client = client or HrevnManagedClient()
        self._handlers: dict[str, ToolHandler] = {
            spec.name: getattr(self.client, spec.handler_name) for spec in TOOL_SPECS
        }
        self._specs: dict[str, ToolSpec] = {spec.name: spec for spec in TOOL_SPECS}

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": spec.name,
                "description": spec.description,
                "inputSchema": spec.input_schema,
            }
            for spec in TOOL_SPECS
        ]

    def call_tool(self, name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
        if name not in self._handlers:
            raise KeyError(f"Unknown HREVN MCP tool: {name}")

        payload = arguments or {}
        try:
            result = self._handlers[name](payload)
        except HrevnApiError as exc:
            error_payload = {
                "status_code": exc.status_code,
                "message": exc.message,
                "details": exc.payload,
            }
            return {
                "content": [
                    {
                        "type": "text",
                        "text": str(error_payload),
                    }
                ],
                "isError": True,
                "structuredContent": error_payload,
            }

        return {
            "content": [
                {
                    "type": "text",
                    "text": str(result),
                }
            ],
            "isError": False,
            "structuredContent": result,
        }
