"""Build the March-July 2026 demand-reduction-by-region figure.

Figure ID: fig-a4d-demand-reduction-by-region
Source data: data/derived/hormuz_a4d_8_demand_splits_blog_table.csv (march_july frame)
Upstream: EIA STEO frozen February 2026 vs August 2026 vintage.
Units: million barrels of consumption below the frozen-February forecast path, 1 Mar - 31 Jul 2026.
Values are forecast-vintage revisions, not measured consumption drops.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/derived/hormuz_a4d_8_demand_splits_blog_table.csv"
OUT_SVG = ROOT / "figures/fig-a4d-demand-reduction-by-region.svg"
OUT_CSV = ROOT / "figures/fig-a4d-demand-reduction-by-region-data.csv"

rows = [r for r in csv.DictReader(open(SRC)) if r["frame"] == "march_july"]
val = {r["geography"]: float(r["value"]) for r in rows
       if r["record_type"] in ("demand_revision", "country_suballocation")}

ASIA = [("China", val["China"], "#1f5f63"),
        ("India", val["India"], "#2f7f83"),
        ("Japan and South Korea",
         val["Japan"] + val["South Korea (bounded suballocation)"], "#4f9a9e"),
        ("Rest of Asia and Oceania",
         val["Asia and Oceania"] - val["China"] - val["India"] - val["Japan"]
         - val["South Korea (bounded suballocation)"], "#7fb8bb")]

BARS = [("Asia and Oceania", val["Asia and Oceania"], ASIA),
        ("Middle East", val["Middle East"], None),
        ("Africa", val["Africa"], None),
        ("Europe", val["Europe"], None),
        ("Eurasia", val["Eurasia"], None),
        ("North America", val["North America"], None),
        ("Central and South America", val["Central and South America"], None)]

W, H = 1400, 700
L, R, TOP = 300, 90, 118
BH, GAP = 52, 22
lo, hi = -20.0, 360.0
span = hi - lo
plot_w = W - L - R
x = lambda v: L + (v - lo) / span * plot_w
TEAL, RED = "#2f6f73", "#8b2f2f"

s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<rect width="100%" height="100%" fill="#ffffff"/>',
     '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#202020}'
     '.title{font-size:30px;font-weight:700}.subtitle{font-size:16px;fill:#4a4a4a}'
     '.label{font-size:15px}.value{font-size:15px;font-weight:700}'
     '.seg{font-size:12px;fill:#ffffff;font-weight:700}.axis{font-size:12px;fill:#666}</style>',
     f'<text x="58" y="48" class="title">Where oil consumption fell</text>',
     f'<text x="58" y="78" class="subtitle">Million barrels below the pre-war forecast path, March-July 2026</text>']

for t in range(0, 361, 60):
    s.append(f'<line x1="{x(t):.1f}" y1="{TOP-14}" x2="{x(t):.1f}" y2="{TOP+len(BARS)*(BH+GAP)-GAP+8}" '
             f'stroke="#e4e4e4" stroke-width="1"/>')
    s.append(f'<text x="{x(t):.1f}" y="{TOP-22}" class="axis" text-anchor="middle">{t}</text>')
s.append(f'<line x1="{x(0):.1f}" y1="{TOP-14}" x2="{x(0):.1f}" y2="{TOP+len(BARS)*(BH+GAP)-GAP+8}" '
         f'stroke="#999" stroke-width="1.4"/>')

y = TOP
for name, v, segs in BARS:
    s.append(f'<text x="{L-18}" y="{y+BH/2+5:.1f}" class="label" text-anchor="end">{name}</text>')
    if segs:
        cur = 0.0
        short = {"Japan and South Korea": "Japan + Korea",
                 "Rest of Asia and Oceania": "Rest of Asia"}
        for sn, sv, col in segs:
            x0, x1 = x(cur), x(cur + sv)
            s.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1-x0:.1f}" height="{BH}" fill="{col}"/>')
            if x1 - x0 > 92:
                s.append(f'<text x="{(x0+x1)/2:.1f}" y="{y+BH/2+4:.1f}" class="seg" '
                         f'text-anchor="middle">{short.get(sn, sn)}</text>')
            cur += sv
        s.append(f'<text x="{x(v)+12:.1f}" y="{y+BH/2+5:.1f}" class="value">{v:.0f}</text>')
    elif v >= 0:
        s.append(f'<rect x="{x(0):.1f}" y="{y}" width="{x(v)-x(0):.1f}" height="{BH}" fill="{TEAL}"/>')
        s.append(f'<text x="{x(v)+12:.1f}" y="{y+BH/2+5:.1f}" class="value">{v:.0f}</text>')
    else:
        s.append(f'<rect x="{x(v):.1f}" y="{y}" width="{x(0)-x(v):.1f}" height="{BH}" fill="{RED}"/>')
        s.append(f'<text x="{x(v)-12:.1f}" y="{y+BH/2+5:.1f}" class="value" text-anchor="end">{v:.0f}</text>')
    y += BH + GAP

s.append('</svg>')
OUT_SVG.write_text("\n".join(s))

with open(OUT_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["geography", "parent", "value_million_bbl", "frame", "measure"])
    for name, v, segs in BARS:
        w.writerow([name, "World", f"{v:.3f}", "march_july",
                    "consumption below frozen-February 2026 EIA STEO path"])
        for sn, sv, _ in (segs or []):
            w.writerow([sn, name, f"{sv:.3f}", "march_july",
                        "consumption below frozen-February 2026 EIA STEO path"])
    w.writerow(["World", "", f"{val['World']:.3f}", "march_july",
                "consumption below frozen-February 2026 EIA STEO path"])
print("wrote", OUT_SVG.name, "and", OUT_CSV.name)
