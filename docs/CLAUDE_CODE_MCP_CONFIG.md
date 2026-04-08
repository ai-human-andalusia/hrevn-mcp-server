# Claude Code MCP Config

Example local MCP configuration for Claude Code.

Depending on how Claude Code is installed, put this JSON in one of:
- `~/.claude.json` for a user-level setup
- `.claude/settings.json` for a project-level setup

Use the one your Claude Code installation already expects.

```json
{
  "mcpServers": {
    "hrevn": {
      "command": "hrevn-mcp-server",
      "env": {
        "HREVN_API_BASE_URL": "https://api.hrevn.com",
        "HREVN_API_KEY": "replace-me"
      }
    }
  }
}
```

## Verify the server first

Before opening Claude Code, verify that the MCP server is installed and can
reach the live backend:

```bash
hrevn-mcp-server --version
hrevn-mcp-server --list-tools
hrevn-mcp-server --self-test
```

## Expected tool path

Once configured, Claude Code should be able to discover and call:
- `baseline_check`
- `profile_validate`
- `generate_bundle`
- `verify_bundle`

## Recommended first test

Ask Claude Code to run `baseline_check` with a minimal payload similar to:

```json
{
  "task_type": "ai_workflow",
  "profile": "eu_readiness_profile",
  "record": {
    "agent_name": "claude_code",
    "summary": "MCP baseline smoke test"
  }
}
```
