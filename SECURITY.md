# Security

## Supported versions

honest-agent is in alpha. Only the latest release gets security fixes.

## Reporting a vulnerability

Please report it privately, through
[GitHub's private vulnerability reporting](https://github.com/jlcoto/the_honest_agent/security/advisories/new),
not in a public issue. A public issue shows everyone how to use the flaw before a fix is
out. A private report gives time to fix it and release, and then the changelog describes
it.

## Using honest-agent safely

honest-agent runs your agent against your warehouse and keeps what it saw. The docs cover
how to keep that safe:

- **Give the MCP server read-only credentials.** honest-agent refuses SQL that isn't a
  read, but it can't check tools that aren't SQL.
  [Connect your agent](https://thehonestagent.dev/docs/connect/#check-the-connection)
- **Keep secrets in `.env`, and `.env` out of git.**
  [Secrets stay in `.env`](https://thehonestagent.dev/docs/connect/#secrets-stay-in-env)
- **Treat results and reports like your data.** They hold what your agent's tools
  returned, which can include rows from your warehouse.
  [What's inside](https://thehonestagent.dev/docs/storing-results/#whats-inside)
- **Never host the report publicly.**
  [Running it for a team](https://thehonestagent.dev/docs/team/)
