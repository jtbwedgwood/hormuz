---
id: "hormuz-k4w.2"
title: "Audit and re-time consumer-country GDP forecasts"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-k4w"
labels:
  - "gdp"
  - "macro"
  - "asia"
  - "forecasts"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T20:30:00Z"
---

# Audit and re-time consumer-country GDP forecasts

## Description

For oil importers we cannot credibly build our own macro models, so take published forecasts
and do the thing forecasters rarely make easy: **say what each one assumed, and what changes
if the assumption is wrong.**

Countries, chosen to match where the repo's demand reduction actually landed (Asia and
Oceania is 346.1 mb of the 570.3 mb March-July world total): **China, India, Indonesia,
Thailand, Vietnam, Philippines, Malaysia, Singapore, Japan, South Korea.** Malaysia and
Indonesia are partly hydrocarbon exporters, so record net-importer status per country — the
sign of the oil-price channel differs.

### Part 1: the forecast audit

For every forecast collected, record:

- Publication date and vintage.
- Whether it incorporates the Hormuz shock at all, and if so through what date of information.
- **The stated assumption.** Most macro forecasts assume an *oil price path*, not a reopening
  date. That is the central methodological fact of this task: the re-timing arithmetic has to
  run through price, not through the Strait.
- **Real or nominal.**
- **Level decline or growth revision** — a cut from +4% to −2% is a 6-point revision, not a
  6% contraction, and is the most likely source of figures circulating publicly.
- Net oil importer or exporter.

Sources: IMF WEO (April 2026, any July update, October 2026 if published by pickup) and
Article IV staff reports; World Bank Global Economic Prospects (June 2026); ADB Asian
Development Outlook; national central banks; OECD Economic Outlook.

### Part 2: re-timing to our two scenarios

Use the scenario definitions from `k4w.1` unchanged. Because forecasts key off price rather
than reopening date, the chain is: scenario → oil price path → GDP effect via a published
elasticity.

- Derive an oil price path for Scenario A and Scenario B. Realized 2026 Brent is already in
  `data/derived/hormuz_r3v_3_price_context_summary.csv`: pre-shock $68.69, March $103,
  April $117 (peak $138.21 on 7 April), May $107, June $85, July $84, 1-11 August $89.
- Compare against each forecast's assumed path and compute the delta.
- Apply published elasticities, **not invented ones**. `hormuz-l8m.5` already holds: ECB
  (May 2026) puts a 10% real oil price rise at roughly 0.2-0.3 pp off euro-area real GDP
  growth in each of the first three years; IMF WP 2017/196 puts a 10% oil inflation shock at
  about 0.4 pp on domestic inflation across 72 countries. **The euro-area GDP elasticity is
  not appropriate for Asia** — source Asia-specific elasticities, separately for net importers
  and net exporters.

### Part 3: the caveat that matters most

Official macro models transmit oil shocks through **price**. The repo's own demand work says
the Asian adjustment was substantially **physical**: refinery and feedstock curtailment,
product export controls, grounded aviation, and India's cooking-fuel scarcity, with road
fuels far more resilient than LPG, naphtha and bitumen. Several governments also suppressed
the price signal directly — India's subsidies and tax cuts, China's price caps and export
controls.

So these forecasts will **systematically understate** the damage wherever rationing was
physical rather than price-mediated, and understate it most in exactly the countries that were
hit hardest. State this plainly next to the numbers. Where the repo has product-level
evidence, note which countries are most affected by the bias rather than leaving it generic.

## Acceptance Criteria

- One table per country: forecast, source, vintage, stated assumption, real/nominal,
  level/growth, net importer or exporter.
- Re-timed estimates under Scenario A and Scenario B, with the elasticity used and its source
  named for each.
- Explicit note of the price-only transmission bias and which countries it most affects.
- No invented elasticities and no unsourced GDP figures. Where no usable forecast exists for
  a country, say so and leave the cell empty rather than interpolating.
- A short reconciliation against the repo's measured March-July demand revisions (China 136.4
  mb, India 64.9, Japan 22.0, Korea 30.6 as a bounded suballocation, Other Asia/Oceania 92.2),
  noting where a forecast implies a demand path inconsistent with what already happened.

## Dependency Notes

- Parent: `hormuz-k4w`
- Blocked by: `hormuz-k4w.1` - scenario definitions must be fixed first
- Related: `hormuz-l8m.5` (macro elasticities already collected), `hormuz-a4d.8` (measured
  regional and country demand revisions), `hormuz-g7t.1` (China balance reconciliation)

## Work Notes

- 2026-08-20: Audited a single comparable current vintage for all ten economies: ADB Asian
  Development Outlook, 8 July 2026. It reports real GDP growth; India is fiscal-year 2026 and
  the other entries are calendar-year. July forecasts/revisions are China 4.6/0.0 pp, India
  6.6/-0.3, Indonesia 5.2/0.0, Thailand 1.8/0.0, Viet Nam 7.2/0.0, Philippines 3.8/-0.6,
  Malaysia 4.6/0.0, Singapore 3.2/+0.2, Japan 0.7/0.0 and Korea 2.6/+0.7.
- 2026-08-20: The audit records ADB's actual assumption rather than assigning a reopening
  date: only partial normalization, gradual 2H26 recovery and $87 average Brent, with gas,
  fertilizer, freight, policy and supply-chain judgment also included. Indonesia and Malaysia
  are not treated as upstream windfall cases; Singapore is labeled a crude-importing
  refining/product-export hub.
- 2026-08-20: Added `scripts/build_k4w_2_consumer_gdp_retiming.py`, which consumes the frozen
  k4w scenario factors unchanged. It generated `data/derived/hormuz_k4w_2_price_paths.csv`
  and `data/derived/hormuz_k4w_2_consumer_gdp_retiming.csv`. The explicit bridge uses observed
  monthly Brent through July, holds the 1-11 August mean for August, then scales the price
  premium over the prewar mean with the canonical shut-in factor. Annual Brent is $87.58 in
  Scenario A base and $90.18 in B, versus ADB's $87.
- 2026-08-20: ADB publishes no country oil-price elasticities. Rather than fabricate them,
  re-timing uses labeled regional bundled scenario slopes derived from published current
  endpoints: April early stabilization ($72 Brent) versus Brief 388 reference ($96 plus gas,
  fertilizer, supply-chain and financial shocks). Per 10% price-equivalent, slopes are -0.06
  pp developing East Asia, -0.18 South Asia, -0.15 developing Southeast Asia and -0.21
  advanced Asia. These are explicitly not structural or oil-only elasticities.
- 2026-08-20: Scenario B re-timed real growth is China 4.58%, India 6.53%, Indonesia 5.15%,
  Thailand 1.75%, Viet Nam 7.15%, Philippines 3.75%, Malaysia 4.55%, Singapore 3.12%, Japan
  0.62% and Korea 2.52%. The small incremental changes reflect that most of the annual price
  shock is already realized and inside ADB's July baseline—not evidence of small physical harm.
- 2026-08-20: Reconciled explicitly to the March-July demand revisions (China 136.4 mb, India
  64.9, Japan 22.0, Korea 30.6 bounded, other Asia/Oceania ex-Korea 92.2) and added country
  physical-rationing warnings. ADB itself states that interrupted imports can make short-run
  effects materially larger than its price-centered model estimates.

## Completion Note

The ten-country forecast audit, identical-scenario price bridge, sourced regional sensitivity,
re-timed estimates, net-import status, measured-demand reconciliation and physical-scarcity
bias audit are complete. No unsourced country coefficient was invented.
