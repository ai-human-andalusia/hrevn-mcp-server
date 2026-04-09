# Antigravity MCP Experiment

Conservative experiment guide for trying HREVN inside Google Antigravity without
claiming more integration than has actually been validated.

## What is real today

- HREVN already has a working stdio MCP server in this repo.
- The MCP server exposes real tools backed by the live managed API:
  - `baseline_check`
  - `profile_validate`
  - `generate_bundle`
  - `verify_bundle`
- The baseline tool calls the real HREVN endpoint:
  - `POST /v1/baseline-check`
- Google's Antigravity codelab explicitly shows that MCP servers can be
  included as agent context with `@` in the agent side panel.

What is **not** asserted here:

- a dedicated Antigravity plugin API
- an official Antigravity guardrail hook
- an Antigravity-specific config file format beyond what your installed preview
  actually exposes in its UI

## Minimal goal

Prove one thing only:

> An Antigravity agent can call HREVN through MCP, receive a real
> `BaselineResult`, and react to `risk_flags`, `missing_required_blocks`, or
> `remedy_payload`.

If that works, the integration path is credible.

## 1. Verify the HREVN MCP server locally

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

## 2. Minimal payload for `baseline_check`

Use this shape:

```json
{
  "task_type": "ai_workflow",
  "profile": "eu_readiness_profile",
  "record": {
    "agent_name": "antigravity",
    "summary": "MCP baseline smoke test for a consequential coding task"
  },
  "metadata": {
    "surface": "google_antigravity",
    "stage": "pre_completion"
  }
}
```

See also:

- `examples/antigravity_baseline_payload.json`

## 3. Minimal Antigravity experiment

The exact UI may evolve across preview builds, so keep the experiment simple:

1. Start Antigravity.
2. Open the agent side panel.
3. Add or reference the local HREVN MCP server from the same environment where
   the `hrevn-mcp-server` command is available.
4. Confirm the agent can discover the `baseline_check` tool.
5. Give the agent a small consequential coding task.
6. Ask it to run `baseline_check` before marking the task complete.

## 4. Prompt to use in Antigravity

```text
Before completing this task, call the HREVN MCP tool `baseline_check`.
Use the payload from the current task context.
If the result contains missing_required_blocks, risk_flags, or a remedy_payload,
do not mark the task complete. Instead, summarize what is missing and what would
need to be corrected before retrying.
Return the HREVN check_id in your final response.
```

## 5. What success looks like

A successful experiment should demonstrate all of the following:

- the agent can discover `baseline_check`
- the tool returns a real `BaselineResult`
- the result includes a real `check_id`
- the agent can read and summarize:
  - `readiness_level`
  - `missing_required_blocks`
  - `risk_flags`
  - `remedy_payload`
- the agent does not treat HREVN as plain prose; it uses the structured output
  to decide what to do next

## 6. What to say publicly if this works

Defensible claim:

> HREVN can be explored in Antigravity through MCP as a verifiable baseline and
> evidence layer around agent workflows. The Antigravity-specific integration
> path is being validated through a live MCP experiment.

Avoid claiming:

- official native integration
- Antigravity-specific guardrail support unless you have directly verified it
- a dedicated Google-supported plugin model for HREVN inside Antigravity

## 7. Why this experiment is enough

This experiment does not need to prove full workflow blocking, pre-deploy policy,
or supervisor orchestration.

It only needs to prove the first credible step:

- Antigravity can call HREVN through MCP
- HREVN returns real structured results
- the agent can react to those results

Once that is proven, deeper orchestration claims can be tested honestly.
