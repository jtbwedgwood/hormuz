---
id: "hormuz-p2k.3"
title: "Classify demand reduction by economic cost tier, by country"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "demand"
  - "qualitative"
  - "durability"
blocked_by: []
blocks:
  - "hormuz-p2k.1"
children: []
owner: "codex-p2k-cost-tiers"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-05T19:37:02Z"
---

# Classify demand reduction by economic cost tier, by country

## Description

Replace the voluntary-versus-involuntary axis used in
`hormuz-inventory-and-demand-residual-stories.md` with an **economic cost** axis. The
existing axis measures agency, which is both unobservable and irrelevant to the durability
question. Grounded aviation is the clearest failure case: a cancelled flight may be an
airline cutting capacity or a passenger declining to book, and no public data separates
those. On a cost axis the same flight is classifiable.

### The three tiers

1. **Essentially costless.** Efficiency improvements and fuel switching using already
   installed capacity. No meaningful output loss. Durable and often permanent.
2. **Continuous drag, indefinitely sustainable.** Real GDP cost, but the economy can carry
   it for a long time once the drag is accepted. This tier does not "break" — it just keeps
   costing. Most forced refinery, feedstock and aviation losses probably land here.
3. **Major economic disruption, or a plausible path to it if the crisis continues.**
   Rationing, cooking-fuel scarcity, sustained industrial shutdown, tourism collapse in
   tourism-dependent economies. This is the tier that defines a break point.

### The key structural finding to test

**The same mechanism lands in different tiers in different countries.** Losing aviation is
tier 2 in Germany and plausibly tier 3 in Thailand. Losing LPG is tier 2 in Japan and tier 3
in India, where it is cooking fuel. The deliverable is therefore a mechanism-by-country
matrix, not a single global split.

This also connects to a likely headline: the geographic distribution of demand destruction
is substantially a **policy choice**, not a pure economic outcome. China restricted refined
product exports, India subsidized and cut taxes, Canada suspended fuel excise duties, and
U.S. consumption actually rose above the frozen path. The barrels came off where there was
neither fiscal space nor refining self-sufficiency.

## Method

Deliberately qualitative and low-fidelity. Do **not** attempt a barrel-level allocation
across the three tiers; the underlying mechanism split is already tier-T3 scenario
allocation, and stacking another allocation on top would manufacture false precision.

Instead, for each major contributing country or region, gather dated news, official and
anecdotal evidence on what actually changed in everyday economic operation, then assign a
tier with a confidence label and the evidence behind it.

Priority geographies, by contribution to the demand gap: China, the Middle East as a region,
residual Asia and Oceania (especially Southeast Asia), India, Africa, Japan, South Korea and
Europe.

## Acceptance Criteria

- A mechanism-by-country tier matrix with dated evidence per cell and an explicit confidence
  label.
- Tier assignments justified by observable disruption to economic operations, not by
  inferred motive.
- Southeast Asia examined specifically. Current project evidence points to the clearest
  explicit restraint policies there (rationing, purchase controls, shortened work or school
  weeks), which is the strongest tier-3 candidate anywhere outside the Middle East.
- An explicit statement of which cells are genuinely unknown.
- No claim that the tiers sum to a barrel total.

## Source Leads

- IEA 2026 energy crisis policy response tracker: https://www.iea.org/data-and-statistics/data-tools/2026-energy-crisis-policy-response-tracker
- Existing mechanism scenarios: `data/derived/hormuz_m8q_12_asia_demand_mechanism_scenarios.csv` and `hormuz_m8q_13_non_asia_demand_mechanisms.csv`
- National statistical releases for industrial production and transport activity
- Trade press on rationing, aviation capacity cuts and petrochemical run cuts

## Work Notes

- 2026-08-05: Claimed after completing `p2k.2`. The deliverable will be an evidence-cell
  matrix rather than a second barrel allocation: geography x mechanism x economic-cost
  tier, with dated evidence, confidence, reversibility, persistence and a separate flag for
  genuinely unknown cells. Southeast Asian countries will be split rather than hidden in
  the residual Asia/Oceania bucket.
- 2026-08-05: Built `scripts/build_p2k_3_demand_cost_tiers.py` and generated
  `data/derived/hormuz_p2k_3_demand_cost_tier_matrix.csv`. The reproducible artifact has 41
  rows: 35 country/mechanism evidence cells, three tier definitions, and three horizon
  syntheses. It validates upstream row IDs against the existing `m8q.12` and `m8q.13`
  mechanism scenario files, but deliberately imports no allocation volumes and exposes no
  barrel-allocation fields. Every evidence row repeats the rule that it cannot be summed or
  used to infer tier shares. Registered the artifact in `data/manifest.csv`.
- 2026-08-05: The agency axis fails empirically and the economic-cost axis does useful work.
  The same nominal conservation mechanism ranges from Singapore public-transit switching
  (tier 1) to Cambodia/Malaysia/Thailand telework and reduced travel (tier 2 or 2-to-3) to
  Lao PDR's three-day school week and Myanmar's fuel rationing (tier 3). Within the
  Philippines, hybrid public-sector work is tier 1-to-2 initially, while reported reductions
  in small-fisher trip hours and days are tier 3 livelihood loss. LPG scarcity is tier 3 in
  India and Kenya because cooking is an essential service and dirty-fuel fallback is costly;
  this should not be narrated as benign fuel switching. China, Japan, and Korea refinery or
  petrochemical run cuts are tier 2 now with a credible tier-3 path through sustained plant
  closures, layoffs, product scarcity, or customer loss. European aviation is tier 2 now,
  while Middle East aviation/tourism hubs and tourism-dependent Thailand have a clearer
  2-to-3 escalation path.
- 2026-08-05: Southeast Asia is resolved across all 11 ASEAN countries rather than left as a
  regional residual: Brunei 2-to-3 (tier 3 if purchase controls bind); Cambodia 2-to-3;
  Indonesia transit/carpooling 1-to-2 and biodiesel 1; Lao PDR 3; Malaysia 2; Myanmar 3;
  Philippines hybrid work 1-to-2 moving toward 2 and fishing 3; Singapore 1 moving toward
  1-to-2 if crowded; Thailand 2-to-3; Timor-Leste unknown now with a 2-to-3 fiscal/supply
  risk; and Viet Nam unknown. This is evidence about operational cost, not a country ranking
  or a quantitative split of the residual demand gap.
- 2026-08-05: Genuinely unknown cells remain explicit. No country-specific realized mobility
  series was found for Japan; South Korean road mobility cannot be separated from policies
  that preserved supply; Timor-Leste's conservation request has no operational measure;
  Viet Nam is absent from the IEA's selected-measures table; and South Africa had credible
  contingency evidence but no realized scarcity cell. Absence of evidence is not coded as
  zero demand reduction.
- 2026-08-05: Exact `p2k.1` horizon handoff: use rows `horizon-6-months`,
  `horizon-12-months`, and `horizon-18-months`. At six months, installed switching remains
  active but bounded; marginal absorption is primarily continuous tier-2 refinery,
  petrochemical, aviation, and mobility drag, with tier-3 pockets already visible in
  cooking, rationing, schooling, and livelihoods. At 12 months, installed switching is a
  persistent cushion rather than fresh headroom; tier-2 costs accumulate and fiscally
  constrained/import-dependent economies increasingly cross into tier 3. At 18 months, the
  marginal absorber is predominantly tier 3 in fragile and low-fiscal-space economies,
  while richer diversified economies continue tier-2 drag and can convert investment into
  new tier-1 switching. These are ordinal durability judgments, not quantities.
- 2026-08-05: Main source breadcrumbs: IEA Southeast Asia Energy Outlook 2026 implemented
  measures table (through 7 May); IEA 2026 crisis policy tracker and July Oil Market Report;
  China NBS June activity release; India PIB LPG and critical-sector allocation releases;
  Japan METI stock-release decision; Kpler and S&P Global operational reporting for Korea;
  Philippines PCO/DOLE workweek releases and Department of Agriculture press clipping;
  Thailand government WFH/travel measures; Indonesia June policy summary; World Bank MENA
  and global June outlooks; African Development Bank shock assessment; AP reporting on Kenya
  LPG-to-charcoal fallback; Egypt and South Africa official releases; and the European
  Commission's 18 May jet-fuel response. URLs and evidence dates are stored per cell in the
  output, not only in these notes.
- 2026-08-05: Validation: script compiles and regenerates 41 unique rows with the 24-field
  schema; all 11 Southeast Asian countries are present; at least one explicit `unknown` is
  required; all upstream context IDs exist; tier values are restricted to the declared
  vocabulary; and forbidden allocation fields are rejected. This satisfies the acceptance
  criteria without claiming that tier cells sum to any barrel total.
