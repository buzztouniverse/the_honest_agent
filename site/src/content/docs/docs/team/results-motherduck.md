---
title: Store results in MotherDuck
description: Keep honest-agent's results in a MotherDuck database.
---

:::caution[An example, not a security review]
This is one setup we tested, shown as an example. Don't copy it blindly: check each step
against your company's security policies, and adapt it before you use it with real data.
See [Your setup, your responsibility](/docs/team/#your-setup-your-responsibility).
:::

honest-agent reads and writes a MotherDuck database directly: nothing to download or
upload, and several jobs can write at the same time.

:::caution[Check MotherDuck's terms first]
Your results hold what your agent's tools returned, which can include data from your
warehouse. Before you create an account, read MotherDuck's
[terms of service](https://motherduck.com/terms-of-service/) and
[privacy policy](https://motherduck.com/privacy-policy/), and check that storing that data
there fits your company's policies.
:::

## 1. Create a service account for the results

A service account is a MotherDuck user for programs rather than people. Give the results
their own, so neither you nor the agent being evaluated writes to them by accident.

1. **Create the service account:** in MotherDuck, Settings → Service Accounts. See
   MotherDuck's guide,
   [Create and configure service accounts](https://motherduck.com/docs/key-tasks/service-accounts-guide/create-and-configure-service-accounts/).
2. **Create a token for it:** on the service account's page, Create token, type
   **Read/Write** (honest-agent writes the results). MotherDuck shows the token only
   once.
3. **Put the token in `HONEST_AGENT_RESULTS_TOKEN`:** in `.env` on your machine, or a
   secret in CI.

## 2. Point the config at it

At the top level of `honest_agent_config.yml`:

```yaml
results_path: md:honest_agent_results
```

The database is created in the service account on the first `run`. Use a database only
for honest-agent: it creates its own tables there (`results`, `traces`, `tool_calls`,
and the `raw` schema).

Check it with `honest-agent debug`: its "Results store" line connects with the token
and says whether the database exists yet.

## 3. Look at the results in MotherDuck (optional)

`honest-agent report` and `honest-agent serve` already show everything. To also query
the results in MotherDuck's own web page, note that the database belongs to the service
account: logged in as yourself, you won't see it until it's shared with you.

Share it from the service account, read-only and only with the people who should see it,
since the results hold what your agent's tools returned. Run this as the service account,
for example in the DuckDB CLI opened with its token (`duckdb "md:?motherduck_token=…"`, or
with `motherduck_token` set in your environment):

```sql
create share honest_agent_results_share from honest_agent_results
    (access restricted, update automatic);
grant read on share honest_agent_results_share to user "you@example.com";
```

Then, logged in as yourself, attach the share with the link `create share` returned:

```sql
attach 'md:_share/...' as honest_agent_results;
select * from honest_agent_results.main.results;
```

`update automatic` keeps the share in step with new runs. See MotherDuck's
[sharing overview](https://motherduck.com/docs/key-tasks/sharing-data/sharing-overview/),
[`create share`](https://motherduck.com/docs/sql-reference/motherduck-sql-reference/create-share/)
and [`grant read on share`](https://motherduck.com/docs/sql-reference/motherduck-sql-reference/grant-access/).

:::caution[Keep the agent away from its own results]
Don't use the agent's MotherDuck token (the one its MCP server uses) for the results:
the agent being evaluated must not be able to change its own results. honest-agent
opens the results with `HONEST_AGENT_RESULTS_TOKEN` only, even when `MOTHERDUCK_TOKEN`
is also set.
:::

:::note
The [GitHub Actions recipe](/docs/team/ci/) uses results in S3. Running it with results
in MotherDuck isn't covered yet.
:::
