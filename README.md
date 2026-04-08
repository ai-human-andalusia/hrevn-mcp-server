# HREVN MCP Server

Minimal MCP server for HREVN, backed by the live managed runtime at `https://api.hrevn.com`.

## Why this exists

For Anthropic and later Codex, MCP is the cleanest way to expose HREVN as real tools rather than only as local helper scripts. This server stays thin on purpose:
- canonical semantics remain in the private HREVN core
- execution remains in the live HREVN managed runtime
- the MCP layer only exposes HREVN capabilities in a standard tool interface

## Included tools

- `baseline_check`
- `profile_validate`
- `generate_bundle`
- `verify_bundle`

## Environment

```bash
export HREVN_API_BASE_URL="https://api.hrevn.com"
export HREVN_API_KEY="replace-me"
```

## Install

```bash
cd hrevn-mcp-server
pip install -e .
```

If you install into a virtual environment, make sure the same virtual
environment is active when you launch Claude Code. Otherwise `hrevn-mcp-server`
may not be on the `PATH` Claude Code uses.

## Run

```bash
hrevn-mcp-server
```

The server uses MCP `stdio` transport.

## Verify before opening Claude Code

```bash
hrevn-mcp-server --version
hrevn-mcp-server --list-tools
hrevn-mcp-server --self-test
```

The self-test runs a live `baseline_check` against the configured HREVN managed API.

If `hrevn-mcp-server` is not found, use the absolute executable path from the
active environment, for example:

```bash
which hrevn-mcp-server
```

and place that path in your Claude Code MCP config instead of the bare command.

## Claude Code MCP example

See:
- `docs/CLAUDE_CODE_MCP_CONFIG.md`
- `examples/baseline_check_payload.json`
- `server.json`

## Recommended first test

Once Claude Code has this MCP server configured, ask it to call:
- `baseline_check`

with the payload in:
- `examples/baseline_check_payload.json`

That should return a real `BaselineResult` from the live HREVN managed API.

## Design rule

This server must not reimplement HREVN truth locally.
It should only expose stable MCP tools that call the managed API.

## Registry readiness

This repo includes:
- `server.json`

as a machine-readable manifest describing the server, transport, environment,
and exposed tools for registry and catalog use.

## Current status

This is a minimal first MCP server aimed at Anthropic-first testing.
It is intentionally thin, real, and compatible with the live managed API path already in production.
