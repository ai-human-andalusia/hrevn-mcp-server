# Antigravity Setup

Practical setup guide for trying the HREVN MCP server inside Google
Antigravity without overstating the current integration level.

## What this setup is for

Use this when you want to:

- add HREVN as a custom MCP server in Antigravity
- run a real `baseline_check` against the live HREVN managed API
- see whether your Antigravity build exposes the tool to the agent

This guide does **not** assume an official Antigravity plugin model for HREVN.

## Prerequisites

- local checkout of this repo
- Python 3.11 or newer
- a valid HREVN runtime API key
- Antigravity running with a trusted workspace

## 1. Verify the MCP server locally first

From this repo:

```bash
cd /path/to/hrevn-mcp-server
export HREVN_API_BASE_URL="https://api.hrevn.com"
export HREVN_API_KEY="replace-with-issued-alpha-key"
PYTHONPATH=src python3 -m hrevn_mcp_server.server --version
PYTHONPATH=src python3 -m hrevn_mcp_server.server --list-tools
PYTHONPATH=src python3 -m hrevn_mcp_server.server --self-test
```

Expected tools:

- `baseline_check`
- `profile_validate`
- `generate_bundle`
- `verify_bundle`

## 2. Open the repo as a trusted workspace in Antigravity

Observed in the current macOS preview flow:

1. Open this repo as a workspace.
2. When Antigravity asks whether you trust the folder authors, choose the
   trusted option for this repo.
3. Open the MCP configuration surface from Antigravity's settings UI.

If Antigravity shows:

> No workspace window available

open the repo as a real workspace first, then return to MCP settings.

## 3. Add HREVN as a custom MCP server

Observed config path in the current preview build:

```text
~/.gemini/antigravity/mcp_config.json
```

Example config:

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

- `examples/antigravity_mcp_config.json`

## 4. Reload the agent session

If the current Antigravity agent instance does not expose MCP tools, try:

1. saving `mcp_config.json`
2. starting a new conversation or agent instance
3. reloading Antigravity if needed

One practical failure mode we observed:

- Antigravity recognized MCP configuration surfaces in the UI
- but the active agent instance still did not inject custom MCP tools into its
  native tool schema

That should be treated as an Antigravity-side limitation, not as evidence that
the HREVN MCP server is broken.

## 5. Minimal prompt

```text
Before completing this task, call the HREVN MCP tool `baseline_check`.
If the result contains missing_required_blocks, risk_flags, or a remedy_payload,
do not mark the task complete. Instead, summarize what is missing and what
would need to be corrected before retrying.
Return the HREVN check_id in your final response.
```

## 6. What a successful test should prove

- Antigravity can see the HREVN MCP server
- the agent can discover `baseline_check`
- the tool returns a real `BaselineResult`
- the response includes a real `check_id`
- the agent can read and summarize:
  - `readiness_level`
  - `missing_required_blocks`
  - `risk_flags`
  - `remedy_payload`

## 7. Honest status line

Use this wording if you need a short public summary:

> HREVN has a working MCP server and can be explored experimentally in
> Antigravity through custom MCP configuration. The Antigravity-specific
> end-to-end tool injection path is still being validated.
