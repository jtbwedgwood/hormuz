#!/usr/bin/env python3
"""Build the standalone blogpost Hormuz ship-tracker widget."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path


INPUT = Path("data/derived/hormuz_2y7_public_daily_tracker.csv")
OUTPUT = Path("blogpost/hormuz-ship-tracker-widget.html")


def load_rows() -> list[dict[str, object]]:
    keep = [
        "date",
        "n_total",
        "n_tanker",
        "n_container",
        "n_dry_bulk",
        "n_general_cargo",
        "n_roro",
        "n_cargo",
        "n_total_7d_avg",
        "n_tanker_7d_avg",
        "pct_baseline_total",
        "pct_baseline_tanker",
    ]
    numeric = set(keep) - {"date"}
    rows: list[dict[str, object]] = []
    with INPUT.open(newline="") as f:
        for row in csv.DictReader(f):
            compact: dict[str, object] = {"date": row["date"]}
            for key in numeric:
                value = float(row[key])
                compact[key] = int(value) if value.is_integer() else round(value, 2)
            rows.append(compact)
    return rows


def build_html(rows: list[dict[str, object]]) -> str:
    data_json = json.dumps(rows, separators=(",", ":"))
    first_date = rows[0]["date"]
    last_date = rows[-1]["date"]
    latest = rows[-1]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Strait of Hormuz Ship Tracker</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172033;
      --muted: #5d687a;
      --line: #d8dee8;
      --soft: #f6f7f9;
      --panel: #ffffff;
      --teal: #087f75;
      --teal-soft: #dff3ef;
      --amber: #b56b12;
      --amber-soft: #fff0d6;
      --red: #b42318;
      --blue: #315c99;
      --grid: #e8edf3;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: #f2f4f7;
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}

    .widget {{
      width: min(1180px, calc(100vw - 28px));
      margin: 24px auto;
      background: var(--panel);
      border: 1px solid #dfe4ec;
      border-radius: 8px;
      box-shadow: 0 18px 45px rgba(28, 39, 60, 0.08);
      overflow: hidden;
    }}

    .topbar {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: start;
      padding: 22px 24px 16px;
      border-bottom: 1px solid var(--line);
    }}

    h1 {{
      margin: 0;
      font-size: 26px;
      line-height: 1.15;
      letter-spacing: 0;
    }}

    .dek {{
      max-width: 760px;
      margin: 7px 0 0;
      color: var(--muted);
      font-size: 15px;
    }}

    .date-readout {{
      min-width: 220px;
      text-align: right;
      color: var(--muted);
      font-size: 13px;
    }}

    .date-readout strong {{
      display: block;
      color: var(--ink);
      font-size: 20px;
      margin-top: 2px;
    }}

    .controls {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) auto;
      gap: 18px;
      padding: 16px 24px 14px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfd;
    }}

    .range-panel {{
      display: grid;
      gap: 10px;
      min-width: 0;
    }}

    .inputs {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }}

    label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 650;
      text-transform: uppercase;
    }}

    input[type="date"] {{
      height: 34px;
      border: 1px solid #cfd7e3;
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      font: inherit;
      font-size: 14px;
      padding: 0 9px;
    }}

    .quick {{
      display: flex;
      gap: 8px;
      align-items: end;
      flex-wrap: wrap;
    }}

    button {{
      height: 34px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      cursor: pointer;
      font: inherit;
      font-size: 13px;
      font-weight: 650;
      padding: 0 11px;
    }}

    button[aria-pressed="true"] {{
      background: #172033;
      border-color: #172033;
      color: #fff;
    }}

    .slider-wrap {{
      position: relative;
      height: 44px;
      padding: 15px 0 0;
    }}

    .track {{
      position: absolute;
      left: 0;
      right: 0;
      top: 23px;
      height: 4px;
      border-radius: 999px;
      background: #d8dee8;
    }}

    .track-active {{
      position: absolute;
      top: 23px;
      height: 4px;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--teal), var(--amber));
      pointer-events: none;
    }}

    input[type="range"] {{
      position: absolute;
      inset: 0;
      width: 100%;
      margin: 0;
      background: transparent;
      pointer-events: none;
      appearance: none;
    }}

    input[type="range"]::-webkit-slider-thumb {{
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 2px solid #fff;
      background: #172033;
      box-shadow: 0 0 0 1px rgba(23, 32, 51, 0.35), 0 3px 8px rgba(23, 32, 51, 0.24);
      pointer-events: auto;
      cursor: ew-resize;
    }}

    input[type="range"]::-moz-range-thumb {{
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 2px solid #fff;
      background: #172033;
      box-shadow: 0 0 0 1px rgba(23, 32, 51, 0.35), 0 3px 8px rgba(23, 32, 51, 0.24);
      pointer-events: auto;
      cursor: ew-resize;
    }}

    .main {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 275px;
      gap: 0;
    }}

    .chart-pane {{
      min-width: 0;
      padding: 18px 20px 18px 24px;
    }}

    .chart-box {{
      width: 100%;
      min-height: 485px;
    }}

    .side {{
      border-left: 1px solid var(--line);
      padding: 18px;
      background: #fcfcfd;
    }}

    .metric {{
      padding: 13px 0;
      border-bottom: 1px solid var(--line);
    }}

    .metric:first-child {{
      padding-top: 0;
    }}

    .metric-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .metric-value {{
      margin-top: 4px;
      color: var(--ink);
      font-size: 28px;
      line-height: 1;
      font-weight: 780;
    }}

    .metric-value small {{
      color: var(--muted);
      font-size: 14px;
      font-weight: 650;
    }}

    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px 18px;
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
    }}

    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .swatch {{
      width: 22px;
      height: 3px;
      border-radius: 99px;
      display: inline-block;
    }}

    .notes {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1px;
      background: var(--line);
      border-top: 1px solid var(--line);
    }}

    .note {{
      background: #fff;
      padding: 15px 18px;
    }}

    .note h2 {{
      margin: 0 0 5px;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0;
    }}

    .note p {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }}

    .tooltip {{
      position: fixed;
      z-index: 10;
      display: none;
      min-width: 178px;
      padding: 9px 10px;
      border: 1px solid #cfd7e3;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.98);
      box-shadow: 0 10px 28px rgba(28, 39, 60, 0.16);
      color: var(--ink);
      font-size: 12px;
      pointer-events: none;
    }}

    .tooltip strong {{
      display: block;
      font-size: 13px;
      margin-bottom: 4px;
    }}

    @media (max-width: 860px) {{
      .topbar,
      .controls,
      .main,
      .notes {{
        grid-template-columns: 1fr;
      }}

      .date-readout {{
        text-align: left;
        min-width: 0;
      }}

      .side {{
        border-left: 0;
        border-top: 1px solid var(--line);
      }}

      .chart-pane {{
        padding: 16px;
      }}
    }}
  </style>
</head>
<body>
  <article class="widget" aria-label="Interactive Strait of Hormuz ship tracker">
    <header class="topbar">
      <div>
        <h1>Strait of Hormuz Ship Traffic</h1>
        <p class="dek">Daily IMF PortWatch chokepoint calls show the collapse and partial recovery in traffic. The chart defaults to 2026; drag the range or use the date fields to compare against earlier years.</p>
      </div>
      <div class="date-readout">
        Selected range
        <strong id="rangeTitle">2026-01-01 to {html.escape(str(last_date))}</strong>
      </div>
    </header>

    <section class="controls" aria-label="Date range controls">
      <div class="range-panel">
        <div class="inputs">
          <label for="startDate">Start</label>
          <input id="startDate" type="date" min="{first_date}" max="{last_date}" value="2026-01-01">
          <label for="endDate">End</label>
          <input id="endDate" type="date" min="{first_date}" max="{last_date}" value="{last_date}">
        </div>
        <div class="slider-wrap">
          <div class="track"></div>
          <div id="trackActive" class="track-active"></div>
          <input id="startRange" type="range" min="0" max="{len(rows) - 1}" value="2557" aria-label="Start date">
          <input id="endRange" type="range" min="0" max="{len(rows) - 1}" value="{len(rows) - 1}" aria-label="End date">
        </div>
      </div>
      <div class="quick" aria-label="Quick date ranges">
        <button type="button" data-preset="2026" aria-pressed="true">2026</button>
        <button type="button" data-preset="shock" aria-pressed="false">Shock</button>
        <button type="button" data-preset="full" aria-pressed="false">Full history</button>
      </div>
    </section>

    <section class="main">
      <div class="chart-pane">
        <div id="chart" class="chart-box" role="img" aria-label="Line chart of daily Strait of Hormuz transits"></div>
        <div class="legend">
          <span><i class="swatch" style="background: var(--teal)"></i>Total calls, 7-day average</span>
          <span><i class="swatch" style="background: var(--amber)"></i>Tanker calls, 7-day average</span>
          <span><i class="swatch" style="background: #6b7280"></i>2019-2024 total baseline</span>
        </div>
      </div>
      <aside class="side" aria-label="Selected range summary">
        <div class="metric">
          <div class="metric-label">Latest selected day</div>
          <div class="metric-value" id="latestTotal">27 <small>total</small></div>
        </div>
        <div class="metric">
          <div class="metric-label">Tanker calls</div>
          <div class="metric-value" id="latestTanker">12 <small>tankers</small></div>
        </div>
        <div class="metric">
          <div class="metric-label">Vs. baseline</div>
          <div class="metric-value" id="latestBaseline">29.8% <small>total</small></div>
        </div>
        <div class="metric">
          <div class="metric-label">Lowest total in range</div>
          <div class="metric-value" id="minTotal">0 <small>calls</small></div>
        </div>
      </aside>
    </section>

    <section class="notes">
      <div class="note">
        <h2>Source</h2>
        <p>IMF PortWatch Daily Chokepoints Data, chokepoint6, fetched into the project on 2026-07-06.</p>
      </div>
      <div class="note">
        <h2>Tanker</h2>
        <p>PortWatch broad vessel class for tanker calls. It is not a barrel count and does not identify the cargo onboard.</p>
      </div>
      <div class="note">
        <h2>Limits</h2>
        <p>Public data show aggregate calls, not ship identities, direction, AIS-dark traffic, or exact products moved.</p>
      </div>
    </section>
  </article>

  <div id="tooltip" class="tooltip"></div>

  <script>
    const DATA = {data_json};
    const MS_PER_DAY = 86400000;
    const baselineTotal = 90.5;
    const shockDate = "2026-02-28";
    const defaultStart = "2026-01-01";
    const parseDate = d => new Date(d + "T00:00:00Z");
    const fmt = new Intl.DateTimeFormat("en-US", {{ month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }});
    const compactFmt = new Intl.DateTimeFormat("en-US", {{ month: "short", day: "numeric", timeZone: "UTC" }});
    const indexByDate = new Map(DATA.map((d, i) => [d.date, i]));
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");
    const startRange = document.getElementById("startRange");
    const endRange = document.getElementById("endRange");
    const rangeTitle = document.getElementById("rangeTitle");
    const trackActive = document.getElementById("trackActive");
    const chart = document.getElementById("chart");
    const tooltip = document.getElementById("tooltip");

    function nearestIndex(dateValue) {{
      if (indexByDate.has(dateValue)) return indexByDate.get(dateValue);
      const target = parseDate(dateValue).getTime();
      let best = 0;
      let bestDistance = Infinity;
      DATA.forEach((row, i) => {{
        const distance = Math.abs(parseDate(row.date).getTime() - target);
        if (distance < bestDistance) {{
          best = i;
          bestDistance = distance;
        }}
      }});
      return best;
    }}

    function setPreset(name) {{
      const ranges = {{
        "2026": ["2026-01-01", DATA[DATA.length - 1].date],
        "shock": ["2026-02-15", "2026-04-30"],
        "full": [DATA[0].date, DATA[DATA.length - 1].date]
      }};
      const [start, end] = ranges[name];
      startRange.value = nearestIndex(start);
      endRange.value = nearestIndex(end);
      syncFromRange();
      document.querySelectorAll("[data-preset]").forEach(button => {{
        button.setAttribute("aria-pressed", button.dataset.preset === name ? "true" : "false");
      }});
    }}

    function enforceOrder() {{
      let a = Number(startRange.value);
      let b = Number(endRange.value);
      if (a > b - 2) {{
        if (document.activeElement === startRange) a = Math.max(0, b - 2);
        else b = Math.min(DATA.length - 1, a + 2);
      }}
      startRange.value = a;
      endRange.value = b;
      return [a, b];
    }}

    function syncFromRange() {{
      const [a, b] = enforceOrder();
      startDate.value = DATA[a].date;
      endDate.value = DATA[b].date;
      render();
    }}

    function syncFromDate() {{
      let a = nearestIndex(startDate.value);
      let b = nearestIndex(endDate.value);
      if (a > b - 2) a = Math.max(0, b - 2);
      startRange.value = a;
      endRange.value = b;
      startDate.value = DATA[a].date;
      endDate.value = DATA[b].date;
      render();
    }}

    function linePath(rows, x, y, key) {{
      return rows.map((row, i) => `${{i === 0 ? "M" : "L"}} ${{x(row)}} ${{y(row[key])}}`).join(" ");
    }}

    function rawBars(rows, x, y, innerH) {{
      const width = Math.max(1, 820 / Math.max(1, rows.length));
      return rows.map(row => {{
        const x0 = Number(x(row)) - width / 2;
        const y0 = Number(y(row.n_total));
        return `<rect x="${{x0.toFixed(1)}}" y="${{y0.toFixed(1)}}" width="${{width.toFixed(1)}}" height="${{(innerH - y0).toFixed(1)}}" fill="#dfe8ed" opacity="0.38"/>`;
      }}).join("");
    }}

    function render() {{
      const a = Number(startRange.value);
      const b = Number(endRange.value);
      const selected = DATA.slice(a, b + 1);
      const latest = selected[selected.length - 1];
      const min = selected.reduce((acc, row) => row.n_total < acc.n_total ? row : acc, selected[0]);
      rangeTitle.textContent = `${{DATA[a].date}} to ${{DATA[b].date}}`;
      document.getElementById("latestTotal").innerHTML = `${{latest.n_total}} <small>total</small>`;
      document.getElementById("latestTanker").innerHTML = `${{latest.n_tanker}} <small>tankers</small>`;
      document.getElementById("latestBaseline").innerHTML = `${{latest.pct_baseline_total}}% <small>total</small>`;
      document.getElementById("minTotal").innerHTML = `${{min.n_total}} <small>${{min.date}}</small>`;
      const leftPct = 100 * a / (DATA.length - 1);
      const rightPct = 100 * b / (DATA.length - 1);
      trackActive.style.left = `${{leftPct}}%`;
      trackActive.style.width = `${{rightPct - leftPct}}%`;

      const w = chart.clientWidth || 860;
      const h = Math.max(430, Math.min(560, Math.round(w * 0.54)));
      const m = {{ top: 34, right: 26, bottom: 54, left: 54 }};
      const innerW = w - m.left - m.right;
      const innerH = h - m.top - m.bottom;
      const dates = selected.map(row => parseDate(row.date).getTime());
      const minDate = dates[0];
      const maxDate = dates[dates.length - 1];
      const maxY = Math.max(120, Math.ceil(Math.max(...selected.map(d => d.n_total), ...selected.map(d => d.n_total_7d_avg), baselineTotal) / 20) * 20);
      const x = row => (m.left + ((parseDate(row.date).getTime() - minDate) / Math.max(MS_PER_DAY, maxDate - minDate)) * innerW).toFixed(1);
      const y = value => (m.top + innerH - (Number(value) / maxY) * innerH).toFixed(1);
      const yTicks = [];
      for (let value = 0; value <= maxY; value += 20) {{
        if (maxY > 140 && value % 40 !== 0) continue;
        const yy = y(value);
        yTicks.push(`<line x1="${{m.left}}" x2="${{w - m.right}}" y1="${{yy}}" y2="${{yy}}" stroke="var(--grid)"/><text x="${{m.left - 10}}" y="${{Number(yy) + 5}}" text-anchor="end" font-size="12" fill="var(--muted)">${{value}}</text>`);
      }}
      const tickCount = w < 700 ? 4 : 7;
      const xTicks = Array.from({{ length: tickCount }}, (_, i) => {{
        const t = minDate + (i / (tickCount - 1)) * (maxDate - minDate);
        const row = selected.reduce((best, candidate) => Math.abs(parseDate(candidate.date).getTime() - t) < Math.abs(parseDate(best.date).getTime() - t) ? candidate : best, selected[0]);
        const xx = x(row);
        return `<line x1="${{xx}}" x2="${{xx}}" y1="${{m.top}}" y2="${{m.top + innerH}}" stroke="#eef2f7"/><text x="${{xx}}" y="${{h - 20}}" text-anchor="middle" font-size="12" fill="var(--muted)">${{compactFmt.format(parseDate(row.date))}}</text>`;
      }}).join("");
      const baselineY = y(baselineTotal);
      const shockVisible = selected[0].date <= shockDate && selected[selected.length - 1].date >= shockDate;
      const shockRow = DATA[nearestIndex(shockDate)];
      const shockX = x(shockRow);
      const svg = `
        <svg viewBox="0 0 ${{w}} ${{h}}" width="100%" height="${{h}}" aria-hidden="true">
          <rect x="0" y="0" width="${{w}}" height="${{h}}" fill="#ffffff"/>
          <g>${{yTicks.join("")}}</g>
          <g>${{xTicks}}</g>
          <g>${{rawBars(selected, x, y, m.top + innerH)}}</g>
          <line x1="${{m.left}}" x2="${{w - m.right}}" y1="${{baselineY}}" y2="${{baselineY}}" stroke="#6b7280" stroke-width="1.7" stroke-dasharray="6 6"/>
          <text x="${{w - m.right}}" y="${{Number(baselineY) - 8}}" text-anchor="end" font-size="12" fill="#4b5563">2019-2024 avg total: 90.5/day</text>
          ${{shockVisible ? `<line x1="${{shockX}}" x2="${{shockX}}" y1="${{m.top}}" y2="${{m.top + innerH}}" stroke="var(--red)" stroke-width="1.8" stroke-dasharray="5 5"/><text x="${{Math.min(w - 142, Number(shockX) + 8)}}" y="${{m.top + 16}}" font-size="12" fill="var(--red)">Feb. 28 shock</text>` : ""}}
          <path d="${{linePath(selected, x, y, "n_total_7d_avg")}}" fill="none" stroke="var(--teal)" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>
          <path d="${{linePath(selected, x, y, "n_tanker_7d_avg")}}" fill="none" stroke="var(--amber)" stroke-width="3.1" stroke-linejoin="round" stroke-linecap="round"/>
          <line x1="${{m.left}}" x2="${{m.left}}" y1="${{m.top}}" y2="${{m.top + innerH}}" stroke="#1f2937"/>
          <line x1="${{m.left}}" x2="${{w - m.right}}" y1="${{m.top + innerH}}" y2="${{m.top + innerH}}" stroke="#1f2937"/>
          <text x="${{m.left}}" y="17" font-size="12" fill="var(--muted)">Daily calls; lines are 7-day averages</text>
          <rect id="hoverRect" x="${{m.left}}" y="${{m.top}}" width="${{innerW}}" height="${{innerH}}" fill="transparent"/>
        </svg>`;
      chart.innerHTML = svg;
      const hover = chart.querySelector("#hoverRect");
      hover.addEventListener("mousemove", event => showTooltip(event, selected, m, innerW, minDate, maxDate));
      hover.addEventListener("mouseleave", hideTooltip);
      document.querySelectorAll("[data-preset]").forEach(button => button.setAttribute("aria-pressed", "false"));
    }}

    function showTooltip(event, rows, m, innerW, minDate, maxDate) {{
      const rect = chart.getBoundingClientRect();
      const xPos = event.clientX - rect.left;
      const ratio = Math.min(1, Math.max(0, (xPos - m.left) / innerW));
      const target = minDate + ratio * (maxDate - minDate);
      const row = rows.reduce((best, candidate) => Math.abs(parseDate(candidate.date).getTime() - target) < Math.abs(parseDate(best.date).getTime() - target) ? candidate : best, rows[0]);
      tooltip.innerHTML = `<strong>${{fmt.format(parseDate(row.date))}}</strong>Total: ${{row.n_total}} calls<br>Tanker: ${{row.n_tanker}} calls<br>7-day total avg: ${{row.n_total_7d_avg}}`;
      tooltip.style.display = "block";
      tooltip.style.left = `${{Math.min(window.innerWidth - 210, event.clientX + 14)}}px`;
      tooltip.style.top = `${{event.clientY + 14}}px`;
    }}

    function hideTooltip() {{
      tooltip.style.display = "none";
    }}

    startRange.addEventListener("input", syncFromRange);
    endRange.addEventListener("input", syncFromRange);
    startDate.addEventListener("change", syncFromDate);
    endDate.addEventListener("change", syncFromDate);
    document.querySelectorAll("[data-preset]").forEach(button => {{
      button.addEventListener("click", () => setPreset(button.dataset.preset));
    }});
    window.addEventListener("resize", () => render());
    startRange.value = nearestIndex(defaultStart);
    endRange.value = DATA.length - 1;
    syncFromRange();
    document.querySelector('[data-preset="2026"]').setAttribute("aria-pressed", "true");
  </script>
</body>
</html>
"""


def main() -> int:
    rows = load_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_html(rows))
    print(f"wrote {OUTPUT} with {len(rows)} embedded rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
