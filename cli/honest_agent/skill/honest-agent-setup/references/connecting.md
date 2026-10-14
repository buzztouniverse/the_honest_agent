# Connecting honest-agent to the agent's MCP server

honest-agent talks to the same MCP server the agent uses. Setting that server up
(creating it, its users, roles and tokens) is the user's job, done with the vendor's
docs. Your part: explain what's needed, point to the right docs, and fill in
honest-agent's side. Never ask for or handle a token's value.

honest-agent's guide for this is "Connect your agent"
(https://thehonestagent.dev/docs/connect/). Use only the part for the user's kind of
server below.

## Advice for every server

- **Read-only credentials.** honest-agent runs the agent with every tool its server
  offers. It refuses SQL that isn't a read (select, show, describe, use) before it
  reaches the server, but it only sees SQL: a tool like `delete_customer(id)` isn't
  checked. A read-only role or token is the real protection.
- **Secrets stay in `.env`.** For a remote server, `init` writes the target with
  `mcp_url: "{{ env_var('<TARGET>_MCP_URL') }}"` and `bearer_token_env:
  <TARGET>_MCP_TOKEN` (e.g. `SNOWFLAKE_MCP_URL`, `SNOWFLAKE_MCP_TOKEN`), and puts both
  names in `.env`. The user fills in the values; `.env` stays out of git.
- **Check with `honest-agent debug`**: its "MCP server" line connects and counts the
  server's tools without calling any.

## By kind of server

- **A local server started by a command** (`mcp_command`): the command runs from the
  config file's folder. It gets only a minimal environment plus the variables listed
  in the target's `mcp_env`, so a server that needs a token from `.env` must list its
  name there.
- **Snowflake managed MCP server** (`mcp_url` + `bearer_token_env`): the user creates
  an MCP server object and a programmatic access token (PAT) for a read-only role.
  Snowflake requires a network policy on the user before it issues a usable PAT;
  the user sets it up with Snowflake's docs, as their account's security rules allow.
  The token goes in the variable the target's `bearer_token_env` names (e.g.
  `SNOWFLAKE_MCP_TOKEN`), not `MCP_BEARER_TOKEN`, which is never sent to a target's
  server.
  Snowflake docs: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp,
  https://docs.snowflake.com/en/sql-reference/sql/create-mcp-server and
  https://docs.snowflake.com/en/user-guide/programmatic-access-tokens and
  https://docs.snowflake.com/en/user-guide/network-policies.
- **MotherDuck** (its hosted server is `https://api.motherduck.com/mcp`; `init`
  pre-fills it in `.env` as `<TARGET>_MCP_URL`): a MotherDuck token, ideally a
  read-only (read scaling) one:
  https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/read-scaling/.
  See the MotherDuck section of https://thehonestagent.dev/docs/connect/.
- **Any other server:** its own docs say how to reach it and authenticate. Fill in
  `mcp_url` (and `bearer_token_env` if it needs a bearer token) or `mcp_command`.
