---
title: Connect your agent
description: Targets, MCP servers and models in honest_agent_config.yml.
---

:::note[Being written]
This page is an outline for now.
:::

## Targets

- One target per agent, like a dbt profile target; `default_target` and `--target`.

## Remote servers: `mcp_url`

- `bearer_token_env`, values read with `env_var()`.
- Snowflake's managed MCP server, MotherDuck, others.

## Local servers: `mcp_command`

- `mcp_env`: the only variables a local server gets.

## Models

- `model` and `judge_model`, per target or at the top level; Anthropic or OpenAI.

## Other target settings

- `default_database` / `default_schema`, `ignore_tools`, `max_tool_steps`, `agent_name`.

## Read-only credentials
