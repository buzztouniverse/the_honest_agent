# Changelog

honest-agent is in alpha: a minor version (0.1 -> 0.2) can break things, and
its notes start with what changed and what to do. A patch version (0.1.0 ->
0.1.1) only fixes bugs.

## v0.1.0 (alpha) — 2026-10-13

The first release for testers. Install it from the tag (see the README).

**What it does:** asks your analytics AI agent known questions through its
MCP server and checks each answer for **accuracy** (is it right?) and
**provenance** (did its SQL read the sources it should?).

- **Commands:** `init` (starter files, `--example` for a demo project that
  needs only a model API key), `debug` (checks the setup without calling a
  model), `ls`, `run`, `report`, `serve`, `logs`, `notify` (Slack) and
  `rebuild`.
- **Models:** Anthropic (Claude) or OpenAI, for the agent and the grader.
- **Grading:** `contains`, `extract_match` (one number or value, with an
  optional tolerance) and `llm_judge`; per-eval thresholds for accuracy and
  provenance.
- **Selecting evals:** `--select` / `--exclude` by id, `tag:` or `category:`,
  like dbt.
- **Results:** a local DuckDB file or a MotherDuck database, with every model
  and tool call kept, so `logs` and `rebuild` work after the fact.
- **CI:** `run` exits 1 when any eval falls below its threshold.
  `docs/hosting.md` has a recipe for running it in GitHub Actions and
  hosting the report behind a sign-in.
- **Setup skill:** `init` can add a skill that helps a coding agent (Claude
  Code, Codex, Cursor and others) set up the project and write the first
  evals with you.
- **Safety:** only read-only SQL (`select`, `show`, `describe`, `use`) reaches
  the agent's MCP server; anything else is refused.

**Known limits:**

- No migrations yet: a results file from a later version may need a manual
  step, which its notes will explain.
- Provenance only sees SQL: an agent that reads data through structured,
  non-SQL tools can't have its sources checked.
- Install from git only; not on PyPI yet.
