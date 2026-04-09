# HREVN MCP Server
<!-- mcp-name: io.github.ai-human-andalusia/hrevn-mcp-server -->

Minimal stdio MCP server for HREVN, backed by the live managed runtime at
`https://api.hrevn.com`.

## Why this exists

This repo exposes HREVN as real MCP tools instead of ad hoc helper scripts.
It stays intentionally thin:

- canonical semantics remain in the HREVN managed runtime
- the MCP layer only exposes stable tool contracts
- consequential results come back as structured output, including
  `risk_flags`, `remedy_payload`, and `check_id`

## Included tools

- `baseline_check`
- `profile_validate`
- `generate_bundle`
- `verify_bundle`

## Environment

```bash
export HREVN_API_BASE_URL="https://api.hrevn.com"
export HREVN_API_KEY="replace-with-issued-alpha-key"
```

Optional environment variables:

- `HREVN_MCP_TIMEOUT_SECONDS`
- `HREVN_MCP_SERVER_NAME`
- `HREVN_MCP_SERVER_VERSION`

## Install

### Editable install

```bash
cd hrevn-mcp-server
python3 -m pip install -e .
```

### From PyPI

```bash
python3 -m pip install hrevn-mcp-server
```

The console entry point is:

```bash
hrevn-mcp-server
```

## Run

```bash
hrevn-mcp-server
```

The server uses MCP `stdio` transport.

## Verify before using a client

```bash
hrevn-mcp-server --version
hrevn-mcp-server --list-tools
hrevn-mcp-server --self-test
```

If you are running directly from source without an installed entry point:

```bash
PYTHONPATH=src python3 -m hrevn_mcp_server.server --list-tools
PYTHONPATH=src python3 -m hrevn_mcp_server.server --self-test
```

The self-test runs a live `baseline_check` against the configured HREVN
managed API.

## Tool contracts

### `baseline_check`

Minimal payload:

```json
{
  "task_type": "ai_workflow",
  "profile": "eu_readiness_profile",
  "record": {
    "agent_name": "example_agent",
    "summary": "baseline smoke test"
  },
  "metadata": {
    "surface": "mcp",
    "stage": "pre_completion"
  }
}
```

### `profile_validate`

Minimal payload:

```json
{
  "profile": "eu_readiness_profile",
  "record": {},
  "metadata": {}
}
```

### `generate_bundle`

Minimal payload:

```json
{
  "record": {},
  "traces": [],
  "options": {
    "include_report_pdf": false
  }
}
```

### `verify_bundle`

Minimal payload:

```json
{
  "source": "/path/to/bundle-or-artifact"
}
```

## Example MCP config

Use a local stdio configuration like this:

```json
{
  "mcpServers": {
    "hrevn": {
      "command": "python3",
      "args": [
        "-m",
        "hrevn_mcp_server.server"
      ],
      "env": {
        "PYTHONPATH": "/ABSOLUTE/PATH/TO/hrevn-mcp-server/src",
        "HREVN_API_BASE_URL": "https://api.hrevn.com",
        "HREVN_API_KEY": "YOUR_HREVN_API_KEY"
      }
    }
  }
}
```

See also:

- [Antigravity setup guide](./docs/ANTIGRAVITY_SETUP.md)
- [Conservative experiment guide](./docs/ANTIGRAVITY_MCP_EXPERIMENT.md)
- [Antigravity MCP config example](./examples/antigravity_mcp_config.json)
- [Antigravity baseline payload](./examples/antigravity_baseline_payload.json)

## Antigravity status

HREVN can already be explored experimentally in Google Antigravity through
custom MCP configuration.

What is already validated:

- the HREVN MCP server runs locally
- the server exposes real tools backed by `https://api.hrevn.com`
- `baseline_check` returns real structured results
- Antigravity preview builds expose MCP configuration surfaces in the UI

What is not claimed yet:

- official native Antigravity integration
- guaranteed MCP tool injection into every Antigravity agent instance
- Antigravity-specific guardrail hooks beyond what has been directly observed

## Registry metadata

This repo includes:

- [server.json](./server.json)

as a machine-readable manifest describing the MCP server, package, transport,
and repository metadata.

## Design rule

This server must not reimplement HREVN truth locally.
It should expose stable MCP tools that call the managed API.
