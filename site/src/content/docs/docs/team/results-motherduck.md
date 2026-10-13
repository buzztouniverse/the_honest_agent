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

1. **Create a MotherDuck service account** that holds only the results.
2. **Put its read/write token in `HONEST_AGENT_RESULTS_TOKEN`:** in `.env` on your
   machine, or a secret in CI.
3. **Point the config at it,** at the top level of `honest_agent_config.yml`:

   ```yaml
   results_path: md:honest_agent_results
   ```

   The database is created on the first `run`.

Check it with `honest-agent debug`: its "Results store" line connects with the token
and says whether the database exists yet.

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
