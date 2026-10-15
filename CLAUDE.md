# Project instructions

## SQL style

Write all SQL in lowercase — keywords included (`select`, `from`, `where`,
`group by`, `join`, etc.), not `SELECT`/`FROM`/`WHERE`. Applies everywhere
SQL is written: seed scripts, tool implementations, storage code, docs.

## Design system

`ui/src/ds/` is copied from the Claude Design project "The Honest Agent
Design System", which is the source of truth and holds files that exist only
there (guidelines, the `ui_kits/dashboard` screens, uploads). Never run the
full `/design-sync` conversion against it: it can overwrite or delete those
files. Sync with targeted file writes only — see `ui/src/ds/README.md` for
the rules and the sync steps.

## Site

`site/` is the landing page and the docs (Astro + Starlight; see
`site/README.md`). It uses `ui/src/ds/` only through its `@ds` alias, so a
design system change affects the site too. Keep `site/` self-contained (it may
move to its own repo): no relative links or imports outside it except `@ds`,
and docs link to code with full GitHub URLs. Check docs claims against the CLI
code and `--help`, not only the README.
