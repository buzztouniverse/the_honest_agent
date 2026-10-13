# Product page handoff: The Honest Agent

This folder is the design handoff for the public product page of `honest-agent`. The designs were made and reviewed screen by screen. They are now ready to build as a real site.

- **Design source:** the Claude Design canvas "First Screen Mockups" (https://claude.ai/artifact/WxrqG2YxWsWQUd9nfGRQh9). The files in `screens/` are standalone exports of the same boards, so they open in any browser.
- **Approved:** every screen in `screens/`. `Main.dc.html` (Option A of the hero) was rejected and is not included.
- **Light mode only.**

## Page order

| # | File | Section | Anchor |
|---|---|---|---|
| 1 | `screens/01-hero.html` | Hero: "Is your AI analytics agent telling you the truth?" | top |
| 2 | `screens/02-connect.html` | Connect: "Works with the MCP server your analytics agent already uses" | `#connect` |
| 3 | `screens/03-loop.html` | "Close the loop, from test to action": the 4-step overview | `#how-it-works` |
| 4 | `screens/04-define.html` | 1 Define: "Define what a right answer looks like" | `#define` |
| 5 | `screens/05-run.html` | 2 Run: "Run your evals in three simple commands" | `#run` |
| 6 | `screens/06-review.html` | 3 Review: "See what failed, and why" | `#review` |
| 7 | `screens/07-improve.html` | 4 Improve: "Catch it, fix it, prove it" | `#improve` |
| 8 | `screens/08-footer.html` | Closing call to action and footer bar | — |

The "Learn more →" links on the loop screen (03) should jump to the matching sections (`#define`, `#run`, `#review`, `#improve`).

## Recommended build

- **Stack:** one Astro project, for example in `site/`. It holds the landing page and the docs, which use **Starlight**. The repo already uses Node and React (`ui/`), so the docs can later embed real design-system components.
- **Hosting:** static, on GitHub Pages or Cloudflare Pages.
- **Interactivity:** the mockups use CSS only (hidden radio inputs, `:checked ~`, `:has()`) so they work without JavaScript. In production, keep the same behaviour. CSS-only is fine; small Astro islands are fine too. The behaviour matters, not the technique.
- **Fidelity:** match the mockups closely in spacing, sizes and copy. The copy was reviewed line by line, so don't rewrite it.

## Global style

- **Page background:** `#EEF0E8` for every section after the hero.
- **Section width and padding:** content max width 1240px. Section padding is `72px 32px 96px`, or `48px 16px 64px` at 900px and below.
- **Fonts** (Google Fonts):
  - Headings: Space Grotesk 500, 40px, letter-spacing -0.02em (30px on phones).
  - Body: Geist.
  - Mono: Geist Mono.
- **Text colours:** `#1C2A22` for primary text, `#4E5C52` for secondary, `#7C877F` for muted.
- **Greens, from the design system** (`ui/src/ds/tokens/colors.css`):
  - Fern `#588157`
  - Sage `#A3B18A`
  - `#3A5A40`
  - `#1F2E26`
- **Accuracy colours** (green, yellow, orange, red) are for data only. They appear inside the report screenshots, never as decoration.
- **Eyebrow:** a 42px circle in fern with a 1.5px sage border, holding the step number in Space Grotesk 700. Next to it, the label in Geist Mono, 18px, uppercase, `#7C877F`. Connect uses the same circle with a dashed sage border and a plug icon instead of a number.
- **Option cards** (Run, Review, Improve, Connect):
  - Border `1px #DAD7CD`, radius 12px.
  - Active card: background `#FBFAF6`, border `#A3B18A`.
  - Only the active card shows its one-line description.
- **Docs links:** fern `#588157`, weight 500, with an arrow "→". Underline on hover.
- **Windows** (terminal, browser, Slack, config) use a soft three-layer shadow: `0 4px 8px rgba(22,33,27,.08), 0 18px 36px rgba(22,33,27,.14), 0 40px 80px -10px rgba(22,33,27,.24)`.
- **Don't use** text shadows or echo effects, side accent bars, or anything cartoonish.
- **Reduced motion:** honour `prefers-reduced-motion` and turn off every animation.
- **Phones:** every section stacks to one column at 900px and below, with text first. There must be no horizontal scroll at 390px.

## Sections

### 1. Hero (`01-hero.html`)
- **Nav:** logo, Docs, Live demo, GitHub.
- **Eyebrow:** "Evals for agentic analytics".
- **Heading and subline:** "Is your AI analytics agent telling you the truth?" / "Catch your agent's mistakes before your team acts on them."
- **Buttons:** Get started, Docs.
- **Video:** a placeholder. **The video's content is not decided yet.**

### 2. Connect (`02-connect.html`)
- **Eyebrow:** "Connect", with the plug icon.
- **Heading:** "Works with the MCP server your analytics agent already uses".
- **Intro:** "Add it to `honest_agent_config.yml` with a URL or a local command, and pick the model your agent runs on. One target per agent, like a dbt profile."
- **Left:** four connector cards stacked vertically:
  - MotherDuck (`mcp_url`)
  - Snowflake (`mcp_url`)
  - Your own server (`mcp_url`)
  - Local server (`mcp_command`)
- **Middle:** thin SVG curves from each card into the robot circle labelled "honest-agent". Only the selected card's curve is fern, with a slow dashed flow; the others are light grey (`#CDD2C6`). This shows that a target uses one server at a time.
- **Under the robot:** a model box reading "Any model · Anthropic or OpenAI". Never name a single model there.
- **Right:** a dark `honest_agent_config.yml` window showing the selected target's YAML, with the connection lines highlighted, plus `honest-agent run --target <name>` underneath. The YAML for each target is in the mockup. The MotherDuck, Snowflake and demo targets match `example_project/honest_agent_config.example.yml`.
- **Phones:** the curves are hidden, and the robot, label and model box are centred.

### 3. The loop (`03-loop.html`)
- **Stepper:** Define, Run, Review, Improve.
- **Window:** it changes per step:
  - Define: an editor where `revenue_1997` is typed in.
  - Run: an animated terminal, where 2 of 4 evals fail.
  - Review: the report.
  - Improve: Slack, "2 of 4".
- Only the active step shows its description and "Learn more →".

### 4. Define (`04-define.html`)
- **Layout:** a three-level table.
  - Level 1: Accuracy and Provenance.
  - Level 2: the grading methods `contains`, `extract_match` and `llm_judge`, as pills. Provenance spans both columns.
  - Level 3: a panel with a chip, one line of explanation, and a real report screenshot with the relevant card highlighted.
- **"</> Show in YAML" toggle:** it swaps the screenshot for the eval YAML, with the key lines highlighted.
- **Link:** "Read the docs on writing evals →".

### 5. Run (`05-run.html`)
- **Layout:** terminal on the left; on the right, the heading, intro and the flow pills `run → report → serve`, which you can click.
  - `run` shows the explainer "Run all your evals, or pick a category, a tag or a single eval." and four options: Everything, `--select category:sales`, `--select tag:critical` and `--select revenue_1997`. Each option types its own command and output into the terminal.
  - `report` types `honest-agent report` and its real output line. Its explanation: "Builds the report from your recent runs into a folder, `honest_agent_report` by default."
  - `serve` types `honest-agent serve`, its output and request logs. Its explanation: "Opens the report in your browser, or host it for your team."
- **Alignment:** the top of the terminal lines up with the heading.
- **Link:** "Read the docs on running evals →" (`#docs-run`).

### 6. Review (`06-review.html`)
- **Layout:** text on the left; on the right, a browser at the placeholder address `evals.yourcompany.com`, scrollable inside, showing real report screenshots.
- **Views:**
  - **Overview:** "Scores for every eval and run. Hover a cell, click it to open the answer."
  - **Compare models:** "Compare your agent's scores across models on the same evals."
  - **Eval details:** "What was expected, what the agent answered, the SQL it ran and its full trace."
- **Hover and click:** hovering the latest heatmap cells shows the report's real tooltip; these hover states are captured images. Clicking `revenue_1997`, or its row in "Below threshold", opens Eval details. The sidebar icons and the report's Back button switch views.
- **Link:** "Read the docs on the report →" (`#docs-report`).

### 7. Improve (`07-improve.html`)
- **Layout:** window on the left, text and three steps on the right.
  - **Get alerted:** a Slack alert in the exact format `cli/honest_agent/notify.py` produces.
  - **Fix your agent:** a teammate's reply slides in: "Maya R.: The agent filtered by ship date and never read `orders`. Pointed it at `orders.o_orderdate` in our semantic layer. Rerunning." The name and message are invented for the mockup.
  - **Prove it:** only the report heatmap. The new 11 Oct column's cells start in the previous day's colours and turn green from top to bottom. Then the real tooltip appears on `revenue_1997`. The animation replays every time the step is opened.
- **Link:** "Read the docs on setting up alerts →" (`#docs-alert`).

### 8. Footer (`08-footer.html`)
- **Closing section:**
  - The robot, then "Is your analytics agent telling the truth?" and "Find out in minutes."
  - `honest-agent init --example` in a dark box with a copy button. Make it actually copy in production.
  - "Sets up a demo agent with six evals. All you need is a model API key. Full install guide →" (`#docs-install`).
  - Buttons: View on GitHub (https://github.com/jlcoto/the_honest_agent) and Read the docs.
- **Footer bar** (`#E3E6DC`):
  - The logo, "The Honest Agent · Open source · MIT license".
  - Links: Docs, GitHub, Contributing, Releases.
  - "Made by José Coto", then LinkedIn and Substack links, then "© 2026".

## Placeholders to fill in

- The docs URLs: `#docs`, `#docs-install`, `#docs-run`, `#docs-report`, `#docs-alert`, and "Read the docs on writing evals" on Define.
- The LinkedIn and Substack URLs, which are `#linkedin` and `#substack` in the footer.
- The hero video.
- "Live demo" in the hero nav, which has no target yet.

## Docs (Starlight) structure

The docs should follow the landing page's anchors:

1. Getting started (install, `init`, `init --example`)
2. Connect your agent (targets, `mcp_url` and `mcp_command`, models)
3. Writing evals
4. Running evals
5. The report
6. Setting up alerts
7. Reference (CLI commands and config keys)

## Assets

- **`assets/robot.png`:** the mascot. It's a bust crop, used in the Slack avatar, the Connect hub and the footer. `design/mascot.svg` in the repo is the auto-traced source.
  - **Don't animate it.** A waving arm was tried and rejected: the SVG's outline is one merged silhouette, so moving the arm leaves seams.
- **`assets/define-*.png`:** report screenshots for Define, with everything outside the target card dimmed.
- **`assets/review-*.webp`:** the Review views and their hover crops.
- **`assets/improve-*.webp`:** the Improve heatmap and its tooltips.
- **Positions:** the coordinates for the hover hotspots and the overlays that turn green are inline in `screens/06-review.html` and `screens/07-improve.html`, as percentages of each image.

### Regenerating the report screenshots
1. Copy `cli/honest_agent/report_ui/` to a folder, and put the sample data in it as `data/report.json`:
   - `report-screenshots/sample-data/report-review.json` for Review.
   - `report-improve.json` for Improve, which adds the 11 Oct run where everything passes.
2. Serve the folder with `python3 -m http.server`.
3. Capture with `report-screenshots/scripts/shot5.py` (Review) and `shot6.py` (Improve). They use Playwright with the sidebar collapsed and the mouse kept off the sidebar. They are scratch scripts: adjust the paths and ports first.
4. `gen5.py` is the script that built `report-review.json`. Its SQL is lowercase, per `CLAUDE.md`.

## Sample data story

The whole page follows one example: agent `sales-agent`, model `claude-sonnet-4-5`, and four evals.

| Eval | Category | Method |
|---|---|---|
| `revenue_1997` | sales | `extract_match` |
| `order_total_1995` | sales | `extract_match` |
| `top_segment` | customers | `contains` |
| `top_nations_last_year` | customers | `llm_judge` |

- `revenue_1997` starts failing on 7 Oct. On 10 Oct it scores accuracy 0.00 and provenance 0.50: the agent filtered `lineitem` by `l_shipdate` and never read `orders`.
- Improve fixes it on 11 Oct, and everything turns green.

**Inconsistencies to fix while building:**
- On 03-loop, the `order_total_1995` title is "Total price of the orders placed in 1995" and its expected answer is `316087761.96`. On Review and Improve the title is "Order total in 1995" and the value is `35055813985.22`. Pick one and use it everywhere.
- On 03-loop, `expected_sources` for `revenue_1997` is `[lineitem, orders]`. On Define it is `[lineitem, warehouse.main.orders]`. Either is valid, but keep it consistent.
- The run IDs differ between 03-loop and 05-run. That's harmless, but they could match.
- The Define screenshots use an older dataset: an expanded sidebar, and the eval `top_ship_mode_1995`. Optionally, regenerate them from `report-review.json` so every screenshot shares the same data.

## Repo rules (from `CLAUDE.md`)

- Write all SQL in lowercase, everywhere.
- `ui/src/ds/` is synced from the Claude Design project "The Honest Agent Design System". Never run a full `/design-sync` against it. Use targeted file writes only (see `ui/src/ds/README.md`).

## CLI facts the page relies on (checked against the repo)

- Commands: `run`, `report`, `serve` (port 8000; opens the browser by default), `notify`, `ls` and `init` (`--example` sets up a demo with six evals).
- `--select` and `--exclude` take an eval id, `tag:x` or `category:x`. `--target` picks a target.
- Results go to `./honest_agent_results/results.duckdb` by default. The report folder is `honest_agent_report` by default. The report shows the last 30 days (`--days`).
- Each target has a single `mcp_url` or `mcp_command`. `model` and `judge_model` can be set per target or at the top level.
- Run output when everything passes: "All evals met their thresholds."
- The Slack alert format comes from `cli/honest_agent/notify.py`.
