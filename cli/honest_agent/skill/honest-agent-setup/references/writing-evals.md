# Writing evals

Evals live in `*.yml` files in the target's evals folder (`evals/` by default; see
`evals_dir` in `honest_agent_config.yml`). Full reference: "Writing evals", "How
provenance is checked" and "Choosing a grading method" in
https://github.com/jlcoto/the_honest_agent/blob/main/example_project/README.md.

## The format

```yaml
version: 1
evals:
  - category: sales                 # a group: its settings apply to its tests
    grading:
      method: extract_match
      min_score: 0.8                # accuracy threshold (default 0.8)
    provenance:
      min_score: 0.7                # provenance threshold (default 0.7)
    tags: [smoke]
    tests:
      # Computed 2026-10-01 with the team's revenue query, for September (the business
      # means the last full calendar month); refresh it every month.
      - id: revenue_last_month
        title: Revenue last month
        prompt: what was revenue last month?
        expected_answer: "1284500.20"
        grading:
          tolerance_percent: 0.01   # within 1% counts as right
        provenance:
          expected_sources: [analytics.fct_revenue]

      # By "top customers" the business means the 5 customers with the most
      # revenue this year.
      - id: top_customers
        title: Top customers
        prompt: who are our top customers?
        expected_answer: "Acme, Globex, Initech, Umbrella and Hooli (by revenue, this year)"
        grading:
          method: llm_judge         # overrides the group's method
        provenance:
          expected_sources: [analytics.fct_revenue, analytics.dim_customer]
```

- A test inherits its group's settings; its own win. `grading` and `provenance` merge
  key by key; `tags` add up.
- **Ids:** `id:` if given, else made from the title (`Revenue last month` becomes
  `revenue_last_month`). Ids must be unique within the evals folder. Suggest writing
  `id:`: rewording a title otherwise changes the id, and the eval loses its history.
- **Selecting:** `honest-agent run --select revenue_last_month` runs one eval;
  `--select tag:smoke`, `--select category:sales`; spaces mean OR, commas AND;
  `--exclude` leaves evals out. `honest-agent ls` lists ids, categories and tags.
- Every eval needs `expected_answer`. `expected_sources` is optional.

## The prompt

Write it the way the people who use the agent ask: their words, their shorthand,
their vagueness. Don't add "give me just the number" or define terms they wouldn't.
The eval exists to see how the agent copes with real questions.

When the question can be read more than one way ("last year": calendar or last full
year? "revenue": gross or net?), don't rewrite it. Ask the user what the business
means, write that into `expected_answer` (saying the reading, as in `top_customers`
above), and use `llm_judge` so an answer that states its assumption can be weighed.
When the business's reading is settled and the answer is one number, `extract_match`
is fine instead; say the reading in a comment, as `revenue_last_month` above does.

## The expected answer

- It comes from the user: they know it, or they run a query you propose (or the
  trusted metric or report) and check the result. Never invent it, and never copy it
  from the agent's answer, even if the user suggests it: then the eval only checks
  the agent agrees with itself.
- Write a number in one form: digits, "." for decimals, no thousands separators,
  currency or units (`1284500.20`, not "1,284,500.20" or "1.284.500,20 €"). A
  percentage is the number shown: 12 for 12%. Written another way, it is compared as
  text and never matches; `honest-agent ls`, `debug` and `run` warn about it. Use
  `tolerance` (an absolute difference) or `tolerance_percent` (0.01 = 1%) when
  rounding is fine.
- If the answer changes over time ("last month", "active customers"), keep the
  wording, note in a comment the date it was computed and how (as in
  `revenue_last_month` above), and tell the user it will need refreshing.

## The grading method

`contains` is the default when no method is set. Pick the method from the shape of
the right answer:

| The right answer is... | Method | Cost |
|---|---|---|
| A value the agent will write exactly one way: a name, a label, an ID, a year | `contains` | Free, no model |
| One number or value that may be formatted or rounded differently | `extract_match` | One model call per eval |
| A list, an explanation, an ambiguous question, or needs judgment | `llm_judge` | One model call per eval |

Each method has limits. Tell the user which one you picked for an eval, why, and its
main limit for that eval, in a sentence, so they can choose differently.

**`contains`** is a character-by-character text match: it lowercases both sides and
checks that the expected text appears somewhere in the answer. Nothing is parsed or
interpreted, so:

- "Acme" passes for "Our top customer is ACME Corp."
- "1284500" fails for "revenue was 1,284,500" and for "$1.28M".
- "4" passes for "we have 400 stores", which is wrong.
- It can't tell a final answer from a value mentioned in passing: "it isn't Acme,
  it's Globex" passes for "Acme".

**`extract_match`**: a model pulls the one value out of the answer and writes a number
in the same form as above, whatever the agent's locale ("1.284.500,20 €" becomes
1284500.20, "12%" becomes 12, "$310.33 million" becomes 310330000); then code compares it. It doesn't judge correctness
itself.

- Without a tolerance the value must be exactly right. Numbers are compared as
  numbers ("1284500.2" equals "1284500.20"), anything else as text, ignoring case.
  When the agent may round differently from your expected value, set `tolerance` or
  `tolerance_percent`. Agents often round big numbers ("about $308 million" for
  307992639.49): an absolute `tolerance: 0.01` fails that, so for amounts like this
  prefer `tolerance_percent` (e.g. 0.005, within 0.5%), and say in a comment what
  rounding is acceptable.
- When the agent's answer gives no clue to its number format ("1,284" alone), the
  model reads "." as the decimal point.
- It expects one value. If the answer lists several numbers, the model may pick the
  wrong one; use `llm_judge` for those.
- Normalizing drops units: "12%" and "12" become the same value. Say the unit in a
  comment.

**`llm_judge`**: a model compares the answer with `expected_answer` and scores it from
0 to 1 with a one-sentence reason. It is the only method with partial credit.

- It is only as strict as `expected_answer`. "Acme and Globex" may let an answer
  with three extra customers pass; "Exactly these 2: Acme, Globex" won't. Write what a
  right answer must contain and what would make it wrong.
- An answer that hedges between several values, or doesn't commit to one, scores 0
  even if one of them is right.
- The score comes from a model, so it can vary a little between runs; a borderline
  answer may pass one day and fail the next. The reason it gives shows why.

## Provenance

Provenance checks that the agent's SQL read the sources it should. The score is the
share of `expected_sources` it read; below `provenance.min_score`, the eval fails.

- **Which source?** Ask the user which table, view or semantic view the team trusts
  for this question: the curated mart rather than raw tables, the semantic view
  rather than hand-written joins. That's a business decision; don't guess it from
  the schema.
- **Only what the answer needs.** Every entry must be read for full marks, so an
  extra one makes a correct answer fail. If any source is fine, leave
  `expected_sources` out: provenance then shows "not checked", never a pass.
- **Where it lives.** An entry is written like a table name in SQL: `orders`,
  `analytics.orders` or `prod.analytics.orders`. `provenance.expected_database` and
  `expected_schema` fill in the parts an entry leaves out. Bare names in the agent's
  SQL are placed by earlier `use` statements, else by the target's
  `default_database`/`default_schema`; without either, a bare name has no known
  location and won't match an expected database or schema.
- **What counts as reading:** a successful `select` (with `with`, `union`, ...).
  `show`, `describe`, catalog queries (`information_schema`, ...), failed queries and
  SQL a tool only generated (without running it) don't count. Any successful select
  does, even a quick `select * from t limit 5` while exploring.
- **Only SQL is seen.** A tool with structured arguments instead of SQL (a
  semantic-layer tool like `query_metrics(metric, grain)`) leaves nothing to read, so a
  correct answer through it scores 0. For such evals leave `expected_sources` out and
  tell the user their provenance can't be checked. Encourage them to open an issue at
  https://github.com/jlcoto/the_honest_agent/issues naming the tool and its arguments,
  so support for it can be added. A tool that keeps SQL in an unusual argument needs
  `provenance.sql_fields: {tool_name: argument}`.

## After writing

`honest-agent ls` confirms the evals load and shows their ids. `honest-agent debug`
checks everything before a run.
