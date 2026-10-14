"""Rewrite the screenshot hotspots in Review.astro and Improve.astro from regen/out/meta.json."""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SEC = HERE.parents[1] / "src/components/sections"
m = json.load(open(HERE / "out/meta.json"))
pct = lambda v, t: f"{v / t * 100:.3f}%"


def rect(x, y, w, h, W, H):
    return f"left:{pct(x, W)};top:{pct(y, H)};width:{pct(w, W)};height:{pct(h, H)}"


def boxr(b, W, H):
    return rect(b[0], b[1], b[2] - b[0], b[3] - b[1], W, H)


# ---------- Review ----------
W, H = m["overview"]["size"]
hv = {h["eval"]: h for h in m["overview"]["hovers"]}
ov = [f'<div class="pg" style="aspect-ratio:{W}/{H}"><img class="base" src="/assets/review-overview.webp" alt="">']
for i, e in enumerate(["revenue_q4", "order_total_2026", "top_segment", "top_nations_last_year"]):
    cell = rect(*hv[e]["cell"], W, H)
    ov.append(
        f'<label class="hs go" for="rv-v3" style="{cell}"></label>'
        if i == 0
        else f'<span class="hs" style="{cell}"></span>'
    )
    ov.append(f'<img class="hv" src="/assets/review-ov_hover_{e}.webp" style="{boxr(hv[e]["box"], W, H)}" alt="">')
ov.append(f'<label class="hs go" for="rv-v3" style="{rect(*hv["row"]["cell"], W, H)}"></label>')
ov.append(f'<img class="hv" src="/assets/review-ov_hover_row.webp" style="{boxr(hv["row"]["box"], W, H)}" alt="">')
ov.append(
    f'<label class="hs go nav" for="rv-v2" style="{rect(*m["overview"]["nav_compare"], W, H)}" title="Model comparison"></label></div>'
)
ov = "".join(ov)

W, H = m["compare"]["size"]
cmp = [f'<div class="pg" style="aspect-ratio:{W}/{H}"><img class="base" src="/assets/review-compare.webp" alt="">']
for h in m["compare"]["hovers"]:
    cell = rect(*h["cell"], W, H)
    cmp.append(
        f'<label class="hs go" for="rv-v3" style="{cell}"></label>'
        if h["col"] == 1
        else f'<span class="hs" style="{cell}"></span>'
    )
    cmp.append(f'<img class="hv" src="/assets/review-cmp_hover_{h["col"]}.webp" style="{boxr(h["box"], W, H)}" alt="">')

p = SEC / "Review.astro"
s = p.read_text()
s, n1 = re.subn(
    r'<div class="pg" style="aspect-ratio:1240/1064">.*?</div>(?=</div><div class="view w2">)', ov, s, flags=re.S
)
s, n2 = re.subn(
    r'<div class="pg" style="aspect-ratio:1240/1354"><img class="base" src="/assets/review-compare.webp" alt="">.*?(?=<label class="hs go nav" for="rv-v1")',
    "".join(cmp),
    s,
    flags=re.S,
)
assert (n1, n2) == (1, 1), (n1, n2)
assert m["compare"]["size"] == [1240, 1354] and m["result"]["size"] == [1240, 1750]
p.write_text(s)

# ---------- Improve ----------
cx, cy, cw, ch = m["improve"]["card"]
rel = lambda b: rect(b[0] - cx, b[1] - cy, b[2], b[3], cw, ch)
relbox = lambda b: rect(b[0] - cx, b[1] - cy, b[2] - b[0], b[3] - b[1], cw, ch)
parts = [
    f'<div class="pg" style="aspect-ratio:{cw:.2f}/{ch:.2f}"><img class="base" src="/assets/improve-heat2.webp" alt="">'
]
for i, cell in enumerate(m["improve"]["cells"]):  # the 11 Oct cells start in the previous run's colour
    parts.append(
        f'<span class="ov" style="{rel(cell["c11"])};background:{cell["c10color"]};--d:{0.90 + 0.28 * i:.2f}s"></span>'
    )
hov = {h["label"]: h for h in m["improve"]["hov"]}
for e in ["revenue_q4", "order_total_2026", "top_segment", "top_nations_last_year"]:
    parts.append(f'<span class="hs" style="{rel(hov[e]["cell"])}"></span>')
    parts.append(f'<img class="hv" src="/assets/improve-hov_{e}.webp" style="{relbox(hov[e]["box"])}" alt="">')
last = 0.90 + 0.28 * len(m["improve"]["cells"]) + 0.30
parts.append(f'<span class="ring" style="{rel(hov["revenue_q4"]["cell"])};--d:{last:.2f}s"></span>')
parts.append(
    f'<img class="auto" src="/assets/improve-hov_revenue_q4.webp" style="{relbox(hov["revenue_q4"]["box"])};--d:{last:.2f}s" alt=""></div>'
)

p = SEC / "Improve.astro"
s = p.read_text()
s, n = re.subn(
    r'<div class="pg" style="aspect-ratio:873\.3333333333334/343\.333">.*?alt=""></div>', "".join(parts), s, flags=re.S
)
assert n == 1, n
p.write_text(s)
print("placed; ring/tooltip delay", round(last, 2))
