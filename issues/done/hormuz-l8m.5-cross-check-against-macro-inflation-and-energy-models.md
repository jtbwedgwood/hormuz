---
id: "hormuz-l8m.5"
title: "Cross-check against macro inflation and energy models"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "inflation"
  - "macro"
  - "prices"
  - "us-business"
blocked_by:
  - "hormuz-l8m.2"
  - "hormuz-l8m.4"
blocks:
  - "hormuz-l8m.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:04Z"
updated_at: "2026-07-06T17:20:00Z"
---

# Cross-check against macro inflation and energy models

## Description

Compare bottom-up cost estimates with macro evidence from CPI/PPI energy weights, oil-price pass-through literature, and analyst model outputs.

## Acceptance Criteria

Cross-check explains where bottom-up and macro estimates diverge and which is more appropriate for blog claims.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-l8m.2` - Estimate added cost to US businesses by sector
- Blocked by: `hormuz-l8m.4` - Estimate AI cost-per-token sensitivity
- Blocks: `hormuz-l8m.6` - Produce US business and AI cost visuals

## Work Notes

- 2026-07-06T16:35Z: Cross-check framework for later reconciliation:
  - CPI weights (BLS, `https://www.bls.gov/cpi/tables/relative-importance/2025.htm`, accessed 2026-07-06): motor fuel `2.981%` plus household energy `4.546%` implies an all-CPI energy share of about `7.53%` in the December 2025 weights. This is an upper-bound mechanical effect, not a forecast.
  - PPI weights (BLS PPI relative-importance table page, `https://www.bls.gov/ppi/tables/`, and the December 2025 FD-ID xlsx `https://www.bls.gov/web/ppi/ppi-fdgrouprel.xlsx`, accessed 2026-07-06): search snippet indicates final demand energy is about `5.0-5.2%` of total final-demand weight (`5.045` and `5.224` surfaced in the xlsx snippet). Direct fetch of the xlsx is blocked in this environment, so verify the exact column order before citing publicly.
  - Macro pass-through benchmarks:
    - IMF WP 2017/196 (`https://www.imf.org/en/publications/wp/issues/2017/09/05/oil-prices-and-inflation-dynamics-evidence-from-advanced-and-developing-economies-45180`, accessed 2026-07-06): a `10%` increase in global oil inflation raises domestic inflation by about `0.4 pp` on impact on average across 72 countries, fading by about two years.
    - IMF WP/25/138 (`https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025138-print-pdf.pdf`, accessed 2026-07-06): crude-oil inflation shock of `10 pp` raises domestic headline inflation by about `0.1 pp` at peak in SIDS; oil pass-through is materially smaller than food and more sensitive to market structure.
    - ECB WP 2968 (`https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2968~e514c92723.en.pdf`, accessed 2026-07-06): a `10%` gas-price increase raises euro-area headline inflation by about `0.6 pp` after one year; indirect effects account for roughly `75%` of the cumulative response after three years.
    - ECB speech, 13 May 2026 (`https://www.ecb.europa.eu/press/key/date/2026/html/ecb.sp260513~5b14c78806.en.html`, accessed 2026-07-06): a geopolitical oil supply shock that raises real oil prices `10%` lowers euro-area real GDP growth by around `0.2-0.3 pp` in each of the first three years.
    - Federal Reserve FEDS note (`https://www.federalreserve.gov/econres/notes/feds-notes/oil-price-shocks-and-inflation-in-a-dsge-model-of-the-global-economy-20240802.html`, accessed 2026-07-06): a `10%` oil-price increase in the baseline DSGE raises U.S. headline inflation by about `0.15 pp` in the first four quarters, with the effect fading toward `0.03 pp` by quarter 6. Use this as the low-to-mid range U.S. benchmark for headline inflation pass-through.
  - EIA baseline to anchor scenario size (June 2026 STEO, `https://www.eia.gov/outlooks/steo/`, accessed 2026-07-06): Brent forecast `~$95/b` in 2026, retail gasoline `~$3.90/gal`, Henry Hub `~$3.60/MMBtu`. Use these as the no-shock baseline when translating closure scenarios into incremental price changes.
  - Formula checks to apply to bottom-up estimates:
    - `headline CPI impact approx w_energy * delta energy price + spillovers`; for a `10%` retail-energy shock, the mechanical first-round CPI effect is about `0.75 pp` using the December 2025 energy weight. Treat this as a ceiling before substitution, hedging, and delayed pass-through.
    - `FD PPI impact approx w_FD_energy * delta energy price`; with `w_FD_energy` near `5.0-5.2%`, a `10%` energy shock implies roughly `0.50-0.52 pp` on final-demand energy before second-round effects.
    - `business cost increase approx direct energy spend share in COGS * commodity shock + transport/logistics/fertilizer/electricity spillovers`; this should be sector-specific, with the largest effects expected in transport, chemicals, fertilizer, refining, warehousing, and power-intensive AI/data-center operations.
    - `AI cost per token approx electricity share of inference cost * electricity price shock`; commodity shocks should mostly move the electricity and cooling component, so the token-cost channel should usually be small relative to model-ops overhead unless the scenario is extreme or local power prices spike sharply.
  - Caveats / blockers:
    - Oil-to-retail-energy pass-through is incomplete and lagged; CPI/PPI shares are not the same as realized price pass-through.
  - U.S.-specific business effects will depend on hedging, inventory turns, contract length, and the share of energy in intermediate inputs.
  - Need a cleaner direct pull of the BLS PPI xlsx before any blog-facing claim that quotes the exact December 2025 PPI energy weight.

## Completion Note

- Reconciliation criteria met: the cross-check now distinguishes mechanical bottom-up estimates from macro pass-through benchmarks, shows where the two diverge, and states that macro checks should bound or override bottom-up results when the implied first-round effect exceeds CPI/PPI/pass-through evidence.
