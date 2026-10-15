// Builds the online demo report into public/report/ (served at /report/): the CLI's
// report UI as `honest-agent report` writes it, the demo data from report-demo/, and a
// banner saying it's a demo, with a link back to the landing page. Runs before
// `astro dev` and `astro build`; public/report/ is generated, so it's gitignored.
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const site = join(dirname(fileURLToPath(import.meta.url)), '..')
const ui = join(site, '..', 'cli', 'honest_agent', 'report_ui')
const demo = join(site, 'report-demo')
const out = join(site, 'public', 'report')

rmSync(out, { recursive: true, force: true })
cpSync(ui, out, { recursive: true })
mkdirSync(join(out, 'data'), { recursive: true })
cpSync(join(demo, 'report.json'), join(out, 'data', 'report.json'))
cpSync(join(demo, 'demo-banner.css'), join(out, 'demo-banner.css'))

const banner =
  '<div class="demo-banner" role="note"><span><strong>Demo report</strong> with sample data: ' +
  'runs of <code>honest-agent init --example</code> over DuckDB\'s TPC-H data.</span>' +
  '<a href="/">← Back to thehonestagent.dev</a></div>'
const index = join(out, 'index.html')
let html = readFileSync(index, 'utf8')
for (const [marker, insert] of [
  ['</head>', '    <link rel="stylesheet" href="./demo-banner.css">\n  </head>'],
  ['<div id="root"></div>', `${banner}\n    <div id="root"></div>`],
]) {
  if (!html.includes(marker)) throw new Error(`report_ui/index.html has no ${marker}; update build-report.mjs`)
  html = html.replace(marker, insert)
}
html = html.replace('<title>The Honest Agent</title>', '<title>Demo report · The Honest Agent</title>')
writeFileSync(index, html)
console.log('Wrote public/report/ (demo report)')
