---
title: Storing results
description: Where honest-agent keeps its results, the three options, and how to choose.
---

Every run stores its results: each eval's scores, and everything the agent and the
grading model sent and received. The report, `logs`, `notify` and `rebuild` all read from
this store. You choose where it lives when you run `init` ("Where should results live?"),
and you can change it later in the config.

| | On your machine (default) | In MotherDuck | In cloud storage (S3, …) |
|---|---|---|---|
| **What it is** | A DuckDB file next to your config | A MotherDuck database | The same DuckDB file, kept in a bucket |
| **You need** | Nothing | A MotherDuck account and a separate token for the results | A bucket and credentials that can read and write one file |
| **Who can run evals** | This machine | Any machine with the token, at the same time | One run at a time, copying the file in and out |
| **Good for** | Trying honest-agent, one person | Teams already on MotherDuck | Teams that keep everything in their own cloud |

Not sure? Start with the default. You can move later; see
[Changing where results live](#changing-where-results-live).

## On your machine

The default. Results go to a file in your project, `honest_agent_results/results.duckdb`,
next to your config.

- **Out of git by itself:** honest-agent puts a `.gitignore` in the folder it creates, so
  the file is never committed by accident.
- **One run at a time:** DuckDB lets one program write to the file at once, which suits
  runs started by hand.
- **Backups are up to you:** the file is the whole history. Losing it loses the history.
- **Another path:** set `results_path` at the top of `honest_agent_config.yml`, or pass
  `--results-path`:

  ```yaml
  results_path: results/evals.duckdb
  ```

## In MotherDuck

```yaml
results_path: md:honest_agent_results
```

honest-agent opens the database with the token in `HONEST_AGENT_RESULTS_TOKEN`, and
creates it on the first `run`. Several machines can write at the same time. Give the
results their own MotherDuck service account and token, never the agent's: the agent being
evaluated must not be able to change its own results.

[Store results in MotherDuck](/docs/team/results-motherduck/) walks through it: the
service account, its token, and how to see the results in MotherDuck's own web page.

## In cloud storage

honest-agent itself only reads and writes a local file. To keep it in Amazon S3 (or Google
Cloud Storage, or Azure Blob Storage), copy the file in before each run and out after, so
`results_path` stays the local default. Only one run may do this at a time.

[Store results in S3](/docs/team/results-s3/) has the bucket, the permissions, and a
script that downloads the file before a run (or starts a new history when there's none
yet).

## What's inside

Whichever you choose, the store holds the same tables:

- `results`, `traces` and `tool_calls`: each eval's scores, its conversation, the SQL it
  ran, and its grading call. The report reads these.
- `raw.runs`, `raw.events` and `raw.evals`: every call exactly as it was sent and
  received. `logs` prints them, and `rebuild` re-scores past runs from them.

Use a store only for honest-agent: it creates and updates these tables.

:::caution[Your results contain what the agent saw]
The store keeps everything each run sent and received, including what the agent's tools
returned: query results (possibly customer rows, names or emails), table listings, and
error messages that can name accounts and roles. Access tokens are never stored. Treat
it like the data your agent can query.
:::

## Changing where results live

Change `results_path` and the next run writes to the new place. The results already
stored don't move with it: the report then starts from an empty history. To keep them,
copy the DuckDB file to the new path, or, for MotherDuck, load the old file into the new
database yourself.
