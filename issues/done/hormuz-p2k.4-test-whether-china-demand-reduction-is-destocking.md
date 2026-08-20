---
id: "hormuz-p2k.4"
title: "Test whether China's demand reduction is partly destocking misclassified"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "china"
  - "demand"
  - "stocks"
  - "accounting-correctness"
blocked_by: []
blocks:
  - "hormuz-p2k.1"
  - "hormuz-p2k.3"
children: []
owner: "p2k_china_destocking"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-05T22:00:00Z"
---

# Test whether China's demand reduction is partly destocking misclassified

## Description

A correctness check on the historical accounting that materially changes the forward
picture, which is why it sits in the durability epic.

**Crude demand is not product consumption.** The ~119.99 mb attributed to China in the EIA
demand gap is *petroleum and other liquid fuels* demand, dominated by refinery intake. If
China imported and ran less crude while covering domestic product supply from inventories
and halted exports, that registers as demand reduction in the global balance even if Chinese
consumers burned an unchanged volume of gasoline and diesel.

Domestic product availability is:

> products available = refinery output + imports - exports + inventory draw

So crude runs down roughly 5.8% year over year in April and 9.1% in May are fully
compatible with no visible change in Chinese daily life, provided exports absorb the
shrinkage and product stocks cover the rest. Refined product exports were reported down
23.6% year over year in May under export controls — roughly 0.25 mb/d, small against a
global gap near 3.6 mb/d, but decisive for *domestic insulation*. Exports were the residual
claimant on Chinese refinery output.

### Why this matters for durability

Demand reduction is indefinitely sustainable; destocking is exhaustible. If a material share
of China's demand slice is actually inventory draw, then that share belongs in an
exhaustible channel and the forward picture is worse than the current accounting implies.

Non-OECD stock reporting is weak enough to make this genuinely plausible. The IEA has no
formal non-OECD submission system, and apparent demand is frequently derived as production
plus imports minus exports plus or minus an estimated stock change.

## Acceptance Criteria

- A comparison of the crude-processing decline against **domestic refined product sales or
  apparent product consumption**, monthly, March-June 2026. If runs fell far more than
  domestic sales, the adjustment was absorbed in the refining, export and inventory layer
  rather than by consumers.
- An explicit estimate, with a range, of how much of the 119.99 mb China demand gap is better
  described as inventory draw than as consumption reduction.
- A statement of how EIA constructs Chinese demand in the STEO, so the misclassification risk
  is characterized rather than assumed.
- Reconciliation with the `hormuz-s49.3` conclusion, which already found commercial and
  operational stock draw to be the dominant Chinese adjustment channel at roughly 85/100
  confidence. That finding and this hypothesis are mutually supporting.
- Any reclassified barrels propagated into `hormuz_r3v_1_confidence_tiered_ledger.csv` and
  the buffer balance sheet in `p2k.1`.

## Source Leads

- NBS monthly energy production releases, April, May, June 2026, already cited in `s49.3`
- NBS and customs refined product output, sales and export series
- Reuters and Bloomberg reporting on the May 2026 refined product export controls
- `issues/done/hormuz-s49.3-evaluate-china-spr-release-claims.md`
- EIA STEO methodology for non-OECD demand estimation

## Work Notes

- 2026-08-05: Claimed for a dedicated China accounting audit. The acceptance test will distinguish petroleum-liquids consumption in EIA's balance from refinery crude throughput and from final domestic product use; it will not assume that lower runs are automatically destocking.
- 2026-08-05: Completed the reproducible reconciliation in `scripts/build_p2k_4_china_demand_reclassification.py`, which generates `data/derived/hormuz_p2k_4_china_demand_reclassification.csv` (49 rows) and is registered once in `data/manifest.csv`.

### Bottom line

- The premise is directionally plausible but quantitatively unproven. EIA publicly describes non-OECD demand as **apparent consumption** and explains that, for Chinese gasoline, it calculates refinery production plus imports minus exports because China does not publish inventory changes. Therefore a product-stock draw can make final use exceed apparent demand.
- The public Chinese/JODI data do **not** observe that product-stock draw. China submits zero in JODI's product-stock-change field while closing stocks are blank; JODI/APEC documentation says China does not submit crude or product stock levels/changes and warns about non-OECD inventory gaps. The zero is therefore a not-submitted encoding, not evidence of no draw.
- The frequently cited roughly 25 mb commercial draw through 7 June is a **crude-stock** estimate. Crude drawn into a refinery is already reflected in refinery/product output; it does not prove that final product use was omitted. This reconciles rather than overturns `hormuz-s49.3`: commercial/operational crude flexibility is strongly supported, while product-stock demand misclassification remains low confidence.
- Recommended accounting treatment is consequently a **sensitivity**, not a base fact: move 0 / 14.972 / 29.943 mb from the China demand-revision slice to opaque inventory/reconciliation for low/base/high. Total absorption must not change, and the reclassified amount must not be added to independently observed global stocks.

### Correct denominator and monthly reconciliation

The upstream 119.992 mb China number covers March-July and includes 29.049 mb of July forecast. The historical March-June denominator is **90.943 mb**.

| Month | EIA February-to-July demand revision (mb) | NBS crude-run shortfall vs 2025 (mb-equivalent, base) | JODI apparent product demand change vs 2025 (mb) | Broad refined-product exports retained vs 2025 (mb-equivalent, base) |
|---|---:|---:|---:|---:|
| March | 3.149 | 10.169 | -1.803 | 4.662 |
| April | 29.435 | 24.664 | -84.427 | 14.916 |
| May | 29.753 | 39.420 | -115.599 | 8.120 |
| June | 28.606 | 80.777 | unavailable in 4 Aug JODI update | 7.528 |
| March-June | **90.943** | **155.030** | -201.830 through May only | **35.226** |

Interpretation:

- Runs fell much more than the STEO demand revision and cannot be used as final consumption. Export suppression retained about 33.0-37.5 mb of broad products domestically; because exports enter apparent demand with a minus sign, this policy **raised** measured domestic availability relative to a no-control case. It is neither destocking nor new global supply.
- The JODI March-May apparent-demand collapse is concentrated in `other oil products` (-159.459 mb), LPG (-40.434 mb) and residual fuel (-19.987 mb), while gasoline (+2.491 mb) and kerosene including jet (+32.394 mb) increased and gas/diesel fell only 12.689 mb. This mix is inconsistent with reading the gross JODI total as a direct daily-life consumption collapse; it reflects refining, feedstock, trade, coverage and missing-stock mechanics.
- JODI's apparent-product identity reconciles the large April-May fall mainly through lower refinery output (-165.462 mb March-May) and product imports (-62.717 mb), partly offset by lower exports (+26.396 mb of apparent domestic availability). It cannot distinguish final sales from product destocking because the stock field is absent.

### Reclassification range

- **Low: 0 mb.** No public product-stock draw is directly observed. This is the defensible confirmed amount.
- **Base: 14.972 mb.** Judgmental midpoint, included only for scenario analysis.
- **High: 29.943 mb.** Deliberately generous ceiling: the 90.943 mb historical STEO gap less 61.0 mb implied by the low end of Daniel Sternoff/CGEP's contemporaneous 0.5-0.6 mb/d gasoline-and-diesel loss estimate over 122 days. Assigning the entire remainder to hidden product stocks leaves nothing for non-road demand, ordinary revision or counterfactual mismatch, so it should not be read as a likely estimate.
- Against the 119.992 mb March-July headline, the same range is 0 / 14.972 / 29.943 mb because July remains forecast and receives no stock claim. The base and high cases are 12.5% and 25.0% of the headline; the remaining 105.020 / 90.049 mb stay in demand reduction, ordinary revision and other unresolved mechanisms.

The range is low confidence. The analyst road-fuel estimate and EIA's frozen-February counterfactual are not perfectly matched; it is used only to ensure the high scenario is bounded by some independent final-use evidence.

### Exact propagation handoff

- Read `inventory-reclassification-march-june-cumulative` for the historical low/base/high values `0 / 14.971593 / 29.943187` million barrels.
- Read `inventory-reclassification-march-july-headline` to apply the same historical allowance against the 119.992047 mb upstream headline without imputing July.
- In `p2k.1`, subtract the selected amount from China's demand-revision/durable-or-costly-adjustment bucket and add it to an **opaque product-stock/reconciliation overlap** bucket. Do not count that new bucket on top of global observed or implied inventory draw; this is a reclassification and the absorption total must remain exactly unchanged.
- In any future `r3v.1` sensitivity, shift the same amount from demand-side T4 to inventory/reconciliation T4. Do not change total T4 or the overall 1,441.5 mb closure. No shared r3v.1 or p2k.1 file was edited by this task.

### Sources and method caveats

- EIA China apparent-demand method: https://www.eia.gov/todayinenergy/detail.php?id=63764
- EIA STEO non-OECD apparent-consumption definition and February/July workbooks: https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf ; https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx ; https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx
- JODI annual secondary-product data and definitions: https://www.jodidata.org/oil/database/data-downloads.aspx ; https://www.jodidata.org/oil/support/user-guide/data-available-in-the-jodi-oil-world-database.aspx
- APEC completeness report documenting absent China crude/product stock reporting: https://www.egnret.ewg.apec.org/sites/default/files/2023-04/day2/2%20Report%20on%20JODI%20Data%20Submissions%20in%20APEC-final.pdf
- NBS March-June processing: https://www.stats.gov.cn/english/PressRelease/202604/t20260417_1963350.html ; https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html ; https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html ; https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html
- Customs/export-control reporting: https://uk.marketscreener.com/news/china-s-march-refined-oil-shipments-fall-after-export-ban-ce7e50d3db80f422 ; https://www.investing.com/news/economy-news/chinas-refined-oil-exports-drop-38-in-april-amid-fuel-restrictions-93CH-4695002 ; https://www.bairdmaritime.com/shipping/tankers/export-rules-cool-down-china-refined-oil-shipments-in-may ; https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d
- Independent final-use and commercial-crude cross-checks: https://apnews.com/article/oil-gasoline-demand-iran-us-iea-report-de45ede94f992da07d35a8b737fdeacf ; https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/

### Validation

- Builder compiles and regenerates with the repository `.venv` and no new dependency.
- Output has 49 rows, 20 uniform columns and 49 unique row IDs.
- Monthly historical EIA rows close exactly to 90.943187 mb; March-July closes to 119.992047 mb.
- Monthly reclassification scenarios close to 0 / 14.971593 / 29.943187 mb.
- Manifest parses with exactly one `hormuz_p2k_4_china_demand_reclassification` registration; dataset IDs remain unique.
