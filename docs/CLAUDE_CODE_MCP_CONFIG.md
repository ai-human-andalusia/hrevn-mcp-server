# Claude Code MCP Config

Example local MCP configuration for Claude Code:

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
