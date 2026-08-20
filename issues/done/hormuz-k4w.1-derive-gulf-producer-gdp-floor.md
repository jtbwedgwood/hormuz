---
id: "hormuz-k4w.1"
title: "Define the two closure scenarios and derive the Gulf producer GDP floor"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-k4w"
labels:
  - "gdp"
  - "macro"
  - "gulf"
  - "scenarios"
blocked_by: []
blocks:
  - "hormuz-k4w.2"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T20:00:00Z"
---

# Define the two closure scenarios and derive the Gulf producer GDP floor

## Description

For the Gulf producers we can do better than quoting someone else's forecast: the direct
hydrocarbon channel is computable from data the repo already holds. Build a **floor** on 2026
real GDP impact from observed and scenario production, and be explicit that it is a floor.

### Part 1: define the scenarios canonically

Write both to a shared artifact that `k4w.2` consumes unchanged.

- **Scenario A — full reopening 30 September 2026.** Requires an explicit recovery ramp, not
  a step. Shut-in wells restart over weeks to months, export chains and tanker positioning
  lag, and EIA's August baseline reaches near-pre-conflict patterns only in early 2027 with
  ~0.6 mb/d still disrupted at end-2027. Publish the ramp as an assumption with a sensitivity
  (e.g. 1-month, 3-month, 6-month convergence).
- **Scenario B — no reopening during 2026.** Hold the current regime. Anchor it on observed
  July shut-in rates rather than the March-May trough, since the current regime is a managed
  partial closure and not the early de facto closure.

### Part 2: the producer floor

Countries: Saudi Arabia, Iraq, Kuwait, UAE, Qatar, Bahrain, Iran.

1. **Monthly output loss by country.** Already available through July in
   `data/derived/hormuz_a4d_2_august_steo_comparison.csv` (August STEO vintage). Cumulative
   March-July shut-ins are Iraq 393.0 mb, Saudi Arabia 370.7, Kuwait 195.8, UAE 133.4,
   Qatar 64.9, Iran 30.6, Bahrain 19.6 — but note EIA's own published Gulf total of 1,318.3 mb
   exceeds the sum of its displayed country rows by 110.4 mb, unexplained. Preserve both.
   As a share of each country's own February output the picture is very different from the
   absolute barrels: Qatar 76%, Bahrain 66%, Iraq 58%, Kuwait 50%, UAE 24%, Saudi Arabia 23%,
   Iran 6%. **That asymmetry is the real finding and it tracks bypass access.**
2. **Extend to December** under both scenarios.
3. **Annual-average 2026 output loss** per country, calendar-weighted from 1 March.
4. **Hydrocarbon value-added share of real GDP** per country. This is the missing input and
   must come from national accounts, not from export value. Sources: IMF Article IV staff
   reports, national statistics offices (Qatar PSA, Saudi GASTAT, UAE FCSC, Iraq CSO),
   World Bank. **Do not reuse** the gross-export-value-over-nominal-GDP shares in
   `docs/hormuz-energy-shock-followups.md`; that document already warns they are not
   national-accounts figures.
5. **Direct real GDP impact** = annual-average output loss x hydrocarbon VA share. Real, so
   no price offset — that is what makes it a floor.

### Part 3: LNG

Qatar and to a lesser extent the UAE cannot be done on oil alone. The repo has supplier-side
capacity (Qatar 9.28 Bcf/d with **no** practical seaborne bypass, UAE Das Island 0.70 Bcf/d
likewise) but **no monthly realized LNG shut-in series**. Build one if the data supports it.
If it does not, publish Qatar and the UAE as oil-only and say so explicitly rather than
proxying LNG from crude.

## Acceptance Criteria

- Scenario definitions in a shared artifact, with the Scenario A ramp stated and sensitivity-tested.
- Per-country annual-average 2026 output loss and direct real GDP floor, both scenarios.
- Hydrocarbon VA shares sourced to national accounts, with the source named per country.
- Every figure labelled real, and labelled level-decline rather than growth-revision.
- **A named list of excluded channels**, so "floor" is honest. At minimum: tourism and
  aviation (the repo documents grounded flights and collapsed tourism), trade and logistics,
  domestic energy-infrastructure outages, war-risk insurance and freight, construction and
  FDI, and the fiscal multiplier from lost government revenue. Note that the fiscal channel
  can cut **both** ways: sovereign wealth drawdown can sustain spending and offset part of
  the hit, which is a real reason Gulf headline GDP falls less than hydrocarbon output.
- Iran flagged separately for data quality; its production and export figures are the least
  reliable in the set and its 6% shut-in share should not be read at face value.

## Dependency Notes

- Parent: `hormuz-k4w`
- Blocks: `hormuz-k4w.2` - which must reuse these scenario definitions unchanged

## Work Notes

- Scratch check worth reproducing properly: at a hydrocarbon VA share of ~35%, Qatar's
  March-July losses alone lock in roughly 32 points of annual-average output loss, about
  -12% real GDP from the direct channel — **before** any August-December loss. Even an
  instant full reopening on 1 September cannot get to the ~-6% figures circulating publicly.
  That strongly suggests published "-6%" numbers are growth revisions, nominal rather than
  real, or stale vintages. Confirming which is a `k4w.2` job, but the arithmetic belongs here.
- The 35% share above is an unsourced placeholder. Replacing it is the point of step 4.
- 2026-08-20: Froze the shared monthly scenario artifact in
  `data/derived/hormuz_k4w_scenarios.csv`. Both scenarios hold each country's July EIA
  shut-in through September. Scenario A then converges linearly to zero over 1, 3, or 6
  months; Scenario B holds July rates through December. The three-month path is the headline.
- 2026-08-20: Added `scripts/build_k4w_1_producer_gdp_floor.py` and generated
  `data/derived/hormuz_k4w_1_producer_gdp_floor.csv`. The build reads the August STEO country
  rows, preserves EIA's 1,318.26 mb published March-July total and the unexplained 110.40 mb
  excess over displayed country rows, and never allocates that discrepancy.
- 2026-08-20: Real hydrocarbon weights and primary breadcrumbs are embedded per row. Sources:
  Saudi GASTAT 2024 annual accounts; Iraq CBI/CSO 2024 annual report; Kuwait CSB constant-price
  tables; UAE FCSC Unified Numbers; Qatar NPC constant-2018-price activity table; Bahrain Open
  Data constant-price national accounts; and the IMF May 2025 regional appendix for Iran.
  Saudi and Iran weights are implied from published real growth contributions/components and
  are lower confidence than direct shares.
- 2026-08-20: Three-month Scenario A direct real-GDP level proxies are Saudi -4.2 pp, Iraq
  -19.4, Kuwait -15.2, UAE -2.5, Qatar -17.9, Bahrain -7.0 and Iran -0.4. Scenario B gives
  -4.9, -22.2, -17.5, -2.5, -20.7, -8.2 and -0.5 pp, respectively. These are level effects,
  not growth revisions.
- 2026-08-20: No defensible monthly realized Qatar/UAE LNG shut-in series was found. Their
  national-account shares combine oil and gas while the EIA loss is crude-only, so those two
  results are explicitly labeled mechanical mixed-sector proxies rather than clean floors.
  The output names all other excluded channels and separately flags Iran's weak data quality.

## Completion Note

Canonical scenarios, restart sensitivity, country output arithmetic, sourced real-value-added
weights, EIA discrepancy preservation, LNG limitation and excluded-channel audit are complete.
