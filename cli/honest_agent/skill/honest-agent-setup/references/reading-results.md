# Reading results

Open this when an eval fails. Don't list the cases to the user: check the logs
yourself, then say which case it looks like and why. `honest-agent logs --eval-id <id>`
shows every call the agent and the grading model made, and the report (`honest-agent report`, then `honest-agent serve`) shows the
same more readably. Full reference: https://thehonestagent.dev/docs/running-evals/.

## Which case is it?

1. **The agent got it wrong.** A real finding: keep the eval; the fix belongs in the
   agent. If the user wants to loosen the eval, explain that it would hide the problem.
2. **The eval is off:** a wrong expected answer, or a grading method that doesn't fit
   the answer (a number checked with `contains`, a rounded amount with no tolerance).
   Fix the eval.
3. **Provenance is too strict:** `expected_sources` lists a table the answer didn't
   need. Remove it.
4. **Provenance can't see the tool:** see below.
5. **Not graded:** the grading model's reply was cut off or unreadable (the reason
   starts with "Not graded"). Run that eval again; if it keeps happening, try another
   `grading_model`.

## When provenance looks wrong

Only bring these up when a provenance score points to them.

- **The SQL was written but not run.** Snowflake's Cortex Analyst returns the SQL it
  wrote without running it; honest-agent shows that SQL but doesn't count it. If the
  agent didn't then run it with another tool, a correct answer scores 0 on provenance.
  For that eval, leave `expected_sources` out and tell the user its provenance can't be
  checked this way.
- **No SQL at all.** honest-agent reads SQL from tool arguments (or results) named
  `sql`, `query` or `statement`. A tool with only structured arguments, such as
  `query_metrics(metric, grain)`, leaves nothing to read. Same fix; the user can open
  an issue at https://github.com/jlcoto/the_honest_agent/issues naming the tool, so
  support can be added.
- **A tool's argument isn't SQL.** If a tool has a `query`-style argument that holds a
  search term (a search tool such as Snowflake's Cortex Search), add the tool to the
  target's `ignore_tools`. A tool that keeps its SQL in an argument with another name
  needs `provenance.sql_fields: {tool_name: argument}` in the eval.
- **What counts as reading a table:** a successful `select`, including a quick one while
  exploring. `show`, `describe`, catalog queries and failed queries don't count.
- **Where a table lives.** If an expected source names a database or schema
  (`prod.analytics.orders`) and the agent wrote a bare name (`from orders`), honest-agent
  places it with an earlier `use`, or with the target's `default_database` and
  `default_schema`. Set those only if the server's connection really starts there: a
  wrong value places tables in the wrong spot without warning. Ask the user to check
  where their server's queries start (for example by asking a client connected to the
  same server to run `select current_database(), current_schema()`).
