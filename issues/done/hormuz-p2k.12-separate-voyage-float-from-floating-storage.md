---
id: "hormuz-p2k.12"
title: "Separate voyage float from discretionary floating storage in oil on water"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "oil-on-water"
  - "stocks"
  - "durability"
blocked_by: []
blocks: []
children: []
owner: "p2k12_float_split"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T00:00:00Z"
---

# Separate voyage float from discretionary floating storage in oil on water

## Description

Oil on water is treated throughout the project as a single quantity inside IEA global observed
stocks. It is not one thing, and conflating its two components distorts both the historical
accounting and the durability analysis.

1. **Voyage float.** The oil that must be in transit at any moment to keep deliveries flowing
   — effectively pipeline fill. It is committed cargo, not a buffer, and it cannot be drawn on.
2. **Discretionary floating storage.** Cargoes deliberately held offshore because they have
   nowhere to go or because the forward curve pays for waiting. This *is* a real buffer.

### This is a period-wide feature, not a June anomaly, and it may close much of the residual

The issue was originally written around the June figure. The monthly data in
`hormuz_m8q_1_monthly_oil_balance.csv` shows the pattern runs through the whole period:

| Month | Onshore change | Oil on water | Net observed | Source scope |
|---|---:|---:|---:|---|
| March | +40 China, +20 Gulf onshore | **+100** | -129 (composite) | Middle East floating, **regional not global** |
| April | **-170** | **+53** | -117 | global split, May OMR |
| May | *no published split found* | *unknown* | -73 | gap to be filled |
| June | **-96** | **+117** | +21 | global split, July OMR |

April is the month nobody has examined. Onshore tanks drew **170 mb**, the largest monthly
onshore draw in the period, but 53 mb went to sea, so the headline recorded 117. That is a
31% suppression of the apparent draw in a month whose global number still looked like a large
draw, so nobody scrutinized it. June merely made the effect visible by flipping the sign.

Oil on water **rose in every month where the split is published, and never fell.** This is a
one-directional suppression of measured drawdown across the period, not noise that averages
out.

**The consequence is potentially large.** At least 270 mb moved onto water across March, April
and June. Restating the 298 mb observed draw on an onshore-accessible basis would give
roughly 568 mb, against EIA's implied 606 mb — which would close most of the 308 mb residual
without invoking hidden tanks or mismeasured demand at all.

That arithmetic is deliberately crude and must not be quoted as-is. The March 100 mb is a
regional Middle East floating figure rather than a global oil-on-water change, May has no
published split, and the monthly values come from different OMR vintages. **Testing whether a
properly constructed onshore-accessible series closes the residual is the single highest-value
task in this issue**, and it should be done before any of the finer decomposition work.

### Why the distinction is decisive here

**Rerouting inflates required voyage float without adding a single usable barrel.** Petroline
to Yanbu and onward to Asia is a far longer voyage than a Hormuz transit, and the IEA reported
a 3.5 mb/d increase in Atlantic Basin crude moving East of Suez — among the longest hauls in
the trade. More barrels are tied up at sea to deliver the same barrels per day. That is
ton-mile inflation, a *cost* of the disruption, not storage.

This makes the published June figure actively misleading. Onshore tanks drew about 96 mb while
oil on water swelled 117 mb, producing a net 21 mb global *build*. Read naively that suggests
the world accumulated inventory in June. The likely reality is that oil became stuck in
longer transits while consumers continued drawing accessible inventory throughout.

The March Gulf floating build of roughly 100 mb is probably the opposite case — genuine
discretionary storage, since exports were physically blocked and the oil had nowhere to go.
So both components are present in this episode, at different times, with opposite meanings.

## Acceptance Criteria

**Priority 1 — complete the monthly series and restate the observed draw**

- A complete March-June 2026 monthly series splitting observed global stock change into
  onshore and oil-on-water components, on a single consistent vintage where possible.
- The May split found or its absence documented explicitly, and the March figure either
  replaced with a genuine global oil-on-water change or clearly retained as regional with the
  limitation stated.
- **An onshore-accessible restatement of the 298 mb observed draw**, with its own low/base/high
  vintage range, presented alongside the existing total-inventory figure rather than replacing
  it.
- An explicit test of how much of the 308.171 mb residual the restated series closes, reported
  even if the answer is "much less than the crude 270 mb estimate suggests."
- The result propagated to `hormuz_r3v_1_confidence_tiered_ledger.csv` and flagged to
  `hormuz-r3v.7`, since a materially smaller residual changes the interagency framing.

**Priority 2 — decompose the oil-on-water change**

- A monthly decomposition into voyage float and discretionary floating storage, or an explicit
  statement of why the split cannot be made from public data. Causal testing of that split is
  scoped separately in `hormuz-p2k.13`; this issue supplies the quantities it tests.
- The March Gulf floating build of ~100 mb assessed as discretionary storage, since exports
  were physically blocked, including whether and when it was subsequently released.
- The June 117 mb build attributed between the two components, with the implication for the
  reported net 21 mb global build stated plainly.

**Priority 3 — propagate**

- Usable-headroom implications carried into `hormuz_p2k_1_absorption_buffer_balance_sheet.csv`:
  any voyage-float component is **not** available headroom and should reduce the usable share
  of apparent global inventory. Note this cuts the opposite way from the residual finding —
  more accessible inventory was consumed than the headline shows, so the durability picture
  worsens even as the residual shrinks. Both should be stated together.
- Residual implications carried into the `r3v` workstream. The existing base scenario assigns
  only 35 mb of the residual to oil-on-water and cargo timing; if the restatement above holds,
  that allocation is far too small and should be revised.

## Notes

Do not overstate achievable precision. Public AIS-derived floating-storage series generally
use a dwell-time threshold, commonly around seven days, to separate storage from transit;
that convention is itself the decomposition, and its threshold is arbitrary. Reporting the
convention used and its sensitivity may be the most honest achievable output.

## Source Leads

- IEA Oil Market Reports April, June and July 2026 for oil-on-water and floating-storage commentary
- IEA readjustment commentary on Atlantic Basin flows East of Suez
- `data/derived/hormuz_m8q_11_inventory_residual_scenarios.csv`, rows `anchor-iea-june-oil-on-water-build` and `scenario-*-oil_on_water_and_cargo_timing_error`
- Kpler and Vortexa published methodology on floating-storage dwell-time thresholds
- IMF PortWatch transit data for voyage-length change: `data/external/portwatch/`

## Work Notes

- 2026-08-06: Claimed by `p2k12_float_split`. Building a consistent-vintage March-June
  onshore/oil-on-water bridge first, then a separately labelled voyage-float versus
  discretionary-storage scenario range. Coordinating causal rerouting quantities with
  `hormuz-p2k.13`; no public AIS series will be represented as observed unless its coverage
  and dwell-time convention are documented.
- 2026-08-06: Completed the 26-row reproducible ledger at
  `data/derived/hormuz_p2k_12_oil_on_water_split.csv` with builder
  `scripts/build_p2k_12_oil_on_water_split.py`.

### The March premise was wrong, and the crude 568 mb result is retired

- The May OMR supplies the missing matched global March split: **oil on water fell 117 mb**
  and on-land stocks drew only **12 mb**, summing to the revised 129 mb global draw. The
  issue's `+100 mb` was Middle East Gulf floating storage, not the global oil-on-water
  change. It is nested inside the global decline and cannot be added to it.
- The April OMR's earlier causal detail reconciles approximately as: oil in transit
  `-181 mb`, Middle East floating storage `+100 mb`, and `-36 mb` of other geography,
  classification, and vintage change, giving the later global `-117 mb` result.
- This correction removes **217 mb** from the issue's crude onshore uplift (`+100` assumed
  versus `-117` reported). The proposed `568 mb` onshore draw is therefore retired.

### March-June accessibility bridge

| Month | Total observed change | Global OOW change | Onshore change | Status |
|---|---:|---:|---:|---|
| March | -129 | -117 | -12 | matched May OMR split |
| April | -117 | +53 | -170 | matched May OMR split |
| May | -73 | -35 / 0 / +35 | -38 / -73 / -108 | July total; OOW sensitivity |
| June | +21 | +117 | -96 | matched July OMR split |

- No public May onshore/oil-on-water split was found. The June OMR's `-143 mb` May total
  was revised to `-73 mb` in July. The `+/-35 mb` OOW sensitivity is anchored to Kpler's
  documented early-May within-month fall from about 1,270 to 1,235 mb, not represented as
  an end-month observation.
- On the latest explicit total headlines, onshore-accessible stocks drew
  **316 / 351 / 386 mb** (low/base/high), versus the existing **298 mb** total-stock draw.
  The wider public-vintage envelope is **273-456 mb** and is deliberately secondary because
  its components are not revised on a common vintage.

### Residual test: apparent narrowing is not valid accounting closure

- Mechanically replacing the 298 mb total-stock comparator with the onshore result appears
  to narrow the 308.171 mb plug by **18 / 53 / 88 mb**, or
  **5.8% / 17.2% / 28.6%**. The base apparent residual would be 255.171 mb.
- That is an **unmatched-boundary calculation**, not a valid global reconciliation. The EIA
  implied stock change and IEA observed comparator are both total-inventory concepts. Oil on
  water is already a measured asset inside the observed total. Removing it only from the
  observed side changes accessibility, not global barrel accounting.
- The valid same-bound closure attributable merely to this restatement is therefore
  **zero**. The headline residual remains **308.171 mb** unless the implied side is also
  reconstructed on an onshore-only boundary. Separate AIS measurement or timing error may
  exist, but the observed OOW change does not establish it. Accordingly, the existing
  35 mb m8q.11 timing-error scenario is not mechanically increased to 53 mb.

### Voyage float versus discretionary storage

- March is partially observed: the `-181 mb` oil-in-transit contraction is voyage-pipeline
  emptying; the `+100 mb` Gulf floating build is plausibly discretionary blocked cargo; a
  `-36 mb` mixed-vintage remainder is not identified.
- April's `+53 mb` is scenario-split at `+40/+53/+66 mb` voyage float and
  `+13/0/-13 mb` discretionary storage. IEA attributes the build to bypass loadings and
  long-haul Atlantic-to-Asia shipments, but no public vessel-level decomposition exists.
- In June, the p2k.13 mechanical test shows normal transit-pipeline refill can account for
  **66 / 111.6 / 152 mb** of the `+117 mb` OOW build: the June Hormuz-flow increase of
  `5.5/6.2/6.9 mb/d` times `12/18/22` laden days. The paired discretionary residual is
  `+51/+5.4/-35 mb`; IEA's qualitative statement that Gulf floating storage was drawn
  favours the high-voyage/negative-discretionary side. Longer-route rerouting is therefore
  not required to explain the June headline.
- Kpler's published API exposes selectable floating-storage minimums of 7, 10, 12, 15, 20,
  30, or 90 days. The voyage/storage boundary is an analyst convention, not a naturally
  observed partition. May remains undecomposed for this reason and because no end-month
  public vessel file was available.

### Propagation and validation

- Added March `-117 mb` global OOW and `-12 mb` on-land rows to the m8q.1 source builder.
- Added non-additive onshore, apparent-boundary, and zero-valid-closure memos to
  `hormuz_r3v_1_confidence_tiered_ledger.csv`; the 308.171 mb top-level plug and all Sankey
  flows remain unchanged.
- Added onshore-accessibility and **zero usable voyage-float headroom** memos to
  `hormuz_p2k_1_absorption_buffer_balance_sheet.csv`. Voyage float remains inside global
  accounting but receives no durable buffer credit.
- All four affected builders compile and regenerate. Monthly identities, paired float
  scenarios, r3v Frame A/Frame B, tier totals, and p2k additive rows validate.
