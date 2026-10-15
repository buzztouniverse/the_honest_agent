"""The 1997/1995 -> Q4 2026 / 2026 rename, shared by the page sources and the sample report data.

Usage: rename.py FILE...   (rewrites in place, fails if any 199x year is left)
"""

import re
import sys

# Order matters: ids first, then titles and prose.
REPLACEMENTS = [
    ("revenue_1997", "revenue_q4"),
    ("order_total_1995", "order_total_2026"),
    ("top_ship_mode_1995", "top_ship_mode_2026"),
    ("Revenue in 1997", "Revenue in Q4 2026"),
    ("revenue in 1997", "revenue in Q4 2026"),
    ("I will sum them for 1997.", "I will sum them for Q4 2026."),
    ("where year(l_shipdate) = 1997", "where l_shipdate >= '2026-10-01' and l_shipdate < '2027-01-01'"),
    ("Order total in 1995", "Order total in 2026"),
    ("orders placed in 1995", "orders placed in 2026"),
    ("line items in 1995", "line items in 2026"),
    ("ship date in 1995", "ship date in 2026"),
    ("shipped in 1995", "shipped in 2026"),
]

for path in sys.argv[1:]:
    s = open(path, encoding="utf-8").read()
    for a, b in REPLACEMENTS:
        s = s.replace(a, b)
    left = sorted(set(re.findall(r".{0,30}\b19\d\d\b.{0,20}", s)))
    # the agent trace stores timings like "duration_ms": 1900; those aren't years
    left = [l for l in left if "duration_ms" not in l and "tokens" not in l]
    if left:
        sys.exit(f"{path}: years left:\n" + "\n".join(left))
    open(path, "w", encoding="utf-8").write(s)
    print("renamed", path)
