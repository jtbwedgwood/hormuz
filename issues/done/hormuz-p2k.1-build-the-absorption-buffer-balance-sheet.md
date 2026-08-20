---
id: "hormuz-p2k.1"
title: "Build the absorption buffer balance sheet"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "buffers"
  - "stocks"
  - "synthesis"
blocked_by: []
blocks: []
children: []
owner: "codex-root"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T19:30:00Z"
---

# Build the absorption buffer balance sheet

## Description

The central deliverable of `hormuz-p2k`. For every absorption channel, record what is left
and how fast it is going, so that exhaustion is arithmetic rather than opinion.

Required columns per channel: current level, floor or ceiling, burn rate, headroom in days
at current rate, what happens at exhaustion, evidence tier.

### The critical modelling point: floors, not zero

Stock buffers do not run to zero. The binding constraints are:

- **Statutory obligations.** IEA members must hold 90 days of net imports. Barrels below
  that line are not politically or legally available in the same way.
- **Operational minimums.** The U.S. SPR has cavern-integrity and pressure limits below
  which the *drawdown rate* degrades before volume is exhausted. Rate capacity can bind
  before volume does, and that distinction matters more than total barrels.
- **Working stock.** Refineries and terminals cannot run on empty tanks; some portion of
  commercial inventory is functionally immobile.

Headroom-above-floor is therefore a much smaller and far more decision-relevant number than
headline stocks. Report both, and lead with headroom.

### Channel-specific treatment

- **Inventory:** the genuinely exhaustible channel. Build on the existing
  `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`.
- **Bypass rerouting:** not a depletion curve. Report utilization against nameplate capacity
  (headroom) plus a vulnerability note. Petroline running near ~5 mb/d against nameplate
  leaves little room, and a successful strike on Yanbu or Fujairah removes the cushion
  instantly rather than gradually.
- **Non-Gulf production:** report announced project timelines and shale response lags. This
  channel improves with time; the question is how fast, not when it fails.
- **Foregone build:** report as spent. See `p2k.5` for remaining forward capacity.
- **Demand reduction:** do not assign a duration. Cross-reference the cost tiers from
  `p2k.3`.

## Acceptance Criteria

- One machine-readable ledger with the columns above, following repo conventions.
- Explicit separation of volume headroom from rate capacity for government stocks.
- A marginal-absorber timeline at 6, 12 and 18 months of continued closure, stating which
  channel carries the incremental barrel at each horizon.
- The T4 portion of the historical accounting carried forward as an explicit
  "unknown buffer, unknown remaining capacity" row rather than assumed exhausted or infinite.
- No price forecast.

## Source Leads

- Existing buffer duration work: `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`
- IEA emergency response and 90-day obligation methodology: https://www.iea.org/topics/oil-security
- EIA weekly SPR stocks and DOE drawdown-rate notices
- Tiered absorption ledger: `data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv`

## Work Notes

- 2026-08-05: Claimed by parent for integration after the first-wave `.2`, `.4`, `.5`, and
  `.7` outputs land. The balance sheet will distinguish stock volume headroom from release
  rate, continuing flows from exhaustible levels, and an explicit unknown-buffer row. The
  6/12/18-month timeline is conditional composition arithmetic, not a price or political
  forecast.
- 2026-08-05: Completed `scripts/build_p2k_1_absorption_buffer_balance_sheet.py`, producing
  `data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv` with 19 rows and 34 uniform
  fields. It is registered once in `data/manifest.csv` and synthesised for readers in
  `docs/hormuz-shock-absorption-durability.md`.

### Balance-sheet conclusions

- The downstream March-June bridge closes exactly to 1,441.477144 mb after applying p2k.4's
  base 14.971593 mb China classification sensitivity: demand falls from 439.228379 to
  424.256786 mb, a separate opaque-product-stock sensitivity carries 14.971593 mb, and the
  298.000000 mb observed draw, 396.077712 mb foregone build and 308.171053 mb unreconciled
  adjustment are unchanged. Low/base/high China values are 0/14.971593/29.943187 mb and
  never enter the observed-stock row.
- The `r3v.1` builder and ledger now expose this as a zero-sum, within-T4 classification
  sensitivity. Demand-side T4 falls by the same amount that opaque-inventory T4 rises, so
  total T4 remains 422.284373 mb and total absorption remains unchanged.
- Bypass is a continuing roughly 3.4 mb/d flow, not a depleting stock. Only 0.2 mb/d of
  low-confidence Iraq sensitivity headroom is identified; Saudi and UAE demonstrated rates
  are at their stated boundaries. Do not infer Saudi export headroom by subtracting Yanbu
  exports from Petroline throughput.
- Foregone-build forward credit is zero. The historical 396.077712 mb was a one-time avoided
  accumulation. The July-vintage August-September balance remains a 131.946171 mb draw; Q4
  2026 and 2027 surpluses are conditional reopening/recovery sensitivities, not banked oil.
- Inventory is the only genuinely exhaustible headline channel, but global usable volume
  above binding floors is not public. IEA's greater-than-1-billion-barrel gross government
  stock statement is retained as a lower-bound memo, never converted to days-to-zero.
- U.S. detail updates through 31 July: SPR 304.809 mb, with a 20.846 mb draw from 26 June
  over 35 days (0.596 mb/d); commercial petroleum excluding SPR 1,220.730 mb, with a
  19.160 mb build over the same window (negative 0.547 mb/d draw). Operational and working
  floors are not public, so days-to-floor remain unknown. DOE's 4.4 mb/d nominal SPR maximum
  is a rate-capacity memo, not usable-volume headroom.
- Historical transfer contributes only process bounds: coordinated-release execution
  windows 30-180 days, administrative stock normalization 12-18 months, and U.S. direct
  purchase refill about 0.06-0.10 mb/d. No transferable demand half-life, rationing
  threshold, bypass-failure probability, recovery time, severity index or price parameter
  was identified.

### Conditional marginal-absorber timeline

- Six months: bypass remains near its ceiling and non-Gulf supply improves slowly; remaining
  stocks are policy-gated. Demand is mainly tier-2 refinery, petrochemical, aviation and
  mobility drag, with tier-3 cooking-fuel, rationing, schooling and livelihood pockets.
- Twelve months: low-cost switching provides persistence rather than much new headroom;
  inventories cannot be assumed refilled. Tier-2 losses accumulate and fragile importers
  increasingly cross into tier 3.
- Eighteen months: current stock burn and unidentified T4 absorption are not extrapolated.
  Richer economies can invest into tier-1 substitution and sustain tier-2 drag; marginal
  adjustment is predominantly tier 3 in low-fiscal-space economies. This horizon extends
  beyond the public EIA monthly path ending December 2027 and is directional only.

### Validation

- All p2k.1-p2k.7 and updated r3v.1 builders compile in the repository `.venv` and regenerate.
- The p2k.1 output has unique row IDs and its additive downstream rows close exactly.
- China reclassification low/base/high cases preserve both the 439.228379 mb original demand
  total and 422.284373 mb T4 total in `r3v.1`.
- Manifest parses with unique dataset IDs; no price forecast or price-to-barrel inference is
  present.

### p2k.8 stock-bound integration

- 2026-08-06: Replaced the refusal to divide by explicit, labelled bounds from p2k.8.
  The U.S. row now gives **0-511.768 days to its unknown operational/policy floor** at the
  latest 0.5956 mb/d rate; 511.768 days is the permissive physical-zero endpoint, not a
  forecast. The IEA statutory floor is zero for the United States because the IEA April
  table classifies it as a net exporter.
- The IEA aggregate memo carries the April public-floor range of 12-58 days of net imports
  and 0-46 days of public headroom above the aggregate 90-day obligation. It also publishes
  the 400/455-day mechanical zero calculations while warning that they are not strict upper
  bounds: the government-stock level is greater than 1 billion barrels and collective flow
  includes obligated-industry stocks.
- Rate capacity now uses GAO's audited December-2025 effective 2.700 mb/d versus 4.415 mb/d
  design snapshot, instead of presenting DOE's 4.4 mb/d nominal maximum without current
  operational context. The U.S. level is identified as the lowest since February 1983.

### p2k.12 accessibility propagation

- 2026-08-06: Added non-additive memos for the 316/351/386 mb onshore-accessible draw and
  voyage float. Required voyage-pipeline fill receives **zero usable-headroom credit** even
  though the same barrels remain assets inside the 298 mb total-stock accounting perimeter.
