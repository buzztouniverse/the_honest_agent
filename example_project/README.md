# example_project

A project that uses the `honest-agent` CLI the way a team would, for developing and
trying it from this repository. It installs `honest-agent` from `../cli` as an
editable dependency (`[tool.uv.sources]` in `pyproject.toml`), so CLI changes show up
here without reinstalling.

Its evals ask real questions of a TPC-H warehouse (`orders`, `lineitem`, `customer`,
...) that `warehouse/seed.py` builds with DuckDB's own generator. By default they run
through the demo MCP server that ships with honest-agent, so provenance is checked
against real SQL and real data.

To try honest-agent in your own folder instead, use `honest-agent init --example`:
see [Getting started](https://thehonestagent.dev/docs/getting-started/).

> **The demo MCP server is for trying honest-agent, not for real data.** It runs any
> read-only SQL against the whole DuckDB file it's given, with no authentication and no
> limits besides a 200-row cap. Like a real server, it doesn't list its tables to the
> agent: the agent finds them itself.

## Setup

```bash
cd example_project
uv sync --python 3.11                                       # installs honest-agent from ../cli, editable
uv run python warehouse/seed.py                             # builds warehouse.duckdb
cp honest_agent_config.example.yml honest_agent_config.yml  # local config, ignored by git
```

Put `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) in a `.env` here or at the repo root:
honest-agent loads the nearest one above the folder it runs in.

## Run

```bash
uv run honest-agent debug     # checks the setup without calling a model
uv run honest-agent run       # the default target, demo
uv run honest-agent report
uv run honest-agent serve
```

## What's here

| Path | What it is |
|---|---|
| `honest_agent_config.example.yml` | The targets: `demo` (default), `motherduck`, `snowflake`. Copy it to `honest_agent_config.yml` and fill in your accounts. |
| `evals/` | Evals for the `demo` target |
| `evals_motherduck/` | The demo questions and a few more, against a copy of the warehouse in MotherDuck |
| `evals_snowflake/` | The demo questions against a copy in Snowflake, plus evals for a semantic view |
| `warehouse/seed.py` | Builds `warehouse.duckdb` from DuckDB's TPC-H generator |

## Docs

- [Writing evals](https://thehonestagent.dev/docs/writing-evals/): the eval file, grading methods, provenance
- [Connect your agent](https://thehonestagent.dev/docs/connect/): targets, models and every setting; [MotherDuck](https://thehonestagent.dev/docs/connect/motherduck/) and [Snowflake](https://thehonestagent.dev/docs/connect/snowflake/) guides
- [Running evals](https://thehonestagent.dev/docs/running-evals/) and [Troubleshooting](https://thehonestagent.dev/docs/troubleshooting/)
