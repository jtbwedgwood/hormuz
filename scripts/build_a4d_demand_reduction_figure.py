"""Build the March-July 2026 demand-reduction-by-region figure.

Figure ID: fig-a4d-demand-reduction-by-region
Source data: data/derived/hormuz_a4d_8_demand_splits_blog_table.csv (march_july frame)
Upstream: EIA STEO, frozen February 2026 vintage vs August 2026 vintage.
Units: million barrels of consumption below the frozen-February forecast path, 1 Mar - 31 Jul 2026.
Percentages are that value over the same region's frozen-February forecast consumption for the
same 153 days, so numerator and denominator share one counterfactual.
Values are forecast-vintage revisions, not measured consumption drops.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/derived/hormuz_a4d_8_demand_splits_blog_table.csv"
OUT_SVG = ROOT / "figures/fig-a4d-demand-reduction-by-region.svg"
OUT_CSV = ROOT / "figures/fig-a4d-demand-reduction-by-region-data.csv"
DAYS = 153

rows = [r for r in csv.DictReader(open(SRC)) if r["frame"] == "march_july"]
keep = ("demand_revision", "country_suballocation")
val = {r["geography"]: float(r["value"]) for r in rows if r["record_type"] in keep}
dem = {r["geography"]: float(r["frozen_february_demand_mb_d"]) for r in rows
       if r["record_type"] in keep and r["frozen_february_demand_mb_d"]}

# Korea is a bounded suballocation, not an EIA country observation: fold it into the remainder.
rest_v = (val["Asia and Oceania"] - val["China"] - val["India"] - val["Japan"])
rest_d = (dem["Asia and Oceania"] - dem["China"] - dem["India"] - dem["Japan"])
pct = lambda v, d: v / (d * DAYS) * 100.0

ASIA = [("China", val["China"], pct(val["China"], dem["China"]), "#1f5f63"),
        ("India", val["India"], pct(val["India"], dem["India"]), "#2f7f83"),
        ("Japan", val["Japan"], pct(val["Japan"], dem["Japan"]), "#4f9a9e"),
        ("Rest of Asia", rest_v, pct(rest_v, rest_d), "#7fb8bb")]

def row(name, segs=None):
    return (name, val[name], pct(val[name], dem[name]), segs)

BARS = [row("Asia and Oceania", ASIA), row("Middle East"), row("Africa"), row("Europe"),
        row("Eurasia"), row("North America"), row("Central and South America")]

W, H = 1600, 720
L, R, TOP = 300, 110, 122
BH, GAP = 56, 22
lo, hi = -20.0, 350.0
plot_w = W - L - R
x = lambda v: L + (v - lo) / (hi - lo) * plot_w
TEAL, RED = "#2f6f73", "#8b2f2f"
bottom = TOP + len(BARS) * (BH + GAP) - GAP + 8
lab = lambda v, p: f"{v:.0f} ({p:.1f}%)"

s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<rect width="100%" height="100%" fill="#ffffff"/>',
     '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#202020}'
     '.title{font-size:30px;font-weight:700}.subtitle{font-size:16px;fill:#4a4a4a}'
     '.label{font-size:15px}.value{font-size:15px;font-weight:700}'
     '.segn{fill:#ffffff;font-weight:700}.segv{fill:#ffffff}.axis{font-size:12px;fill:#666}</style>',
     '<text x="58" y="48" class="title">Where oil consumption fell</text>',
     '<text x="58" y="78" class="subtitle">Million barrels below the pre-war forecast path, '
     'March-July 2026, with share of forecast consumption</text>']

for t in range(0, 351, 50):
    s.append(f'<line x1="{x(t):.1f}" y1="{TOP-14}" x2="{x(t):.1f}" y2="{bottom}" stroke="#e4e4e4" stroke-width="1"/>')
    s.append(f'<text x="{x(t):.1f}" y="{TOP-22}" class="axis" text-anchor="middle">{t}</text>')
s.append(f'<line x1="{x(0):.1f}" y1="{TOP-14}" x2="{x(0):.1f}" y2="{bottom}" stroke="#999" stroke-width="1.4"/>')

y = TOP
for name, v, p, segs in BARS:
    s.append(f'<text x="{L-18}" y="{y+BH/2+5:.1f}" class="label" text-anchor="end">{name}</text>')
    if segs:
        cur = 0.0
        for sn, sv, sp, col in segs:
            x0, x1 = x(cur), x(cur + sv)
            s.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1-x0:.1f}" height="{BH}" fill="{col}"/>')
            w = x1 - x0
            fn, fv = (13, 12) if w > 120 else (11, 10)
            if w > 62:
                cx = (x0 + x1) / 2
                s.append(f'<text x="{cx:.1f}" y="{y+BH/2-3:.1f}" class="segn" font-size="{fn}" text-anchor="middle">{sn}</text>')
                s.append(f'<text x="{cx:.1f}" y="{y+BH/2+14:.1f}" class="segv" font-size="{fv}" text-anchor="middle">{lab(sv, sp)}</text>')
            cur += sv
        s.append(f'<text x="{x(v)+12:.1f}" y="{y+BH/2+5:.1f}" class="value">{lab(v, p)}</text>')
    elif v >= 0:
        s.append(f'<rect x="{x(0):.1f}" y="{y}" width="{x(v)-x(0):.1f}" height="{BH}" fill="{TEAL}"/>')
        s.append(f'<text x="{x(v)+12:.1f}" y="{y+BH/2+5:.1f}" class="value">{lab(v, p)}</text>')
    else:
        s.append(f'<rect x="{x(v):.1f}" y="{y}" width="{x(0)-x(v):.1f}" height="{BH}" fill="{RED}"/>')
        # negative bars are short; label to the right of the zero line to clear the row label
        s.append(f'<text x="{x(0)+12:.1f}" y="{y+BH/2+5:.1f}" class="value">{lab(v, p)}</text>')
    y += BH + GAP

s.append('</svg>')
OUT_SVG.write_text("\n".join(s))

with open(OUT_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["geography", "parent", "value_million_bbl", "pct_of_frozen_february_forecast_consumption",
                "frame", "measure"])
    for name, v, p, segs in BARS:
        w.writerow([name, "World", f"{v:.3f}", f"{p:.2f}", "march_july",
                    "consumption below frozen-February 2026 EIA STEO path"])
        for sn, sv, sp, _ in (segs or []):
            w.writerow([sn, name, f"{sv:.3f}", f"{sp:.2f}", "march_july",
                        "consumption below frozen-February 2026 EIA STEO path"])
    w.writerow(["World", "", f"{val['World']:.3f}", f"{pct(val['World'], dem['World']):.2f}",
                "march_july", "consumption below frozen-February 2026 EIA STEO path"])
print("wrote", OUT_SVG.name)
