---
id: "hormuz-p2k.6"
title: "Scope whether historical supply shocks can inform durability at all"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "historical-comparison"
  - "method"
  - "scoping"
blocked_by: []
blocks: []
children: []
owner: "p2k_foregone_build"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T00:30:00Z"
---

# Scope whether historical supply shocks can inform durability at all

## Description

`hormuz-4j7` already built a historical shock comparison, but it ranks shocks by **severity**
using a rubric. The durability epic needs something different and harder: evidence about
**how long coping measures last and how they decay**. It is not obvious that any historical
episode supplies that.

This is deliberately filed as a **scoping task with a real option to conclude "no usable
comparandum."** That conclusion, stated clearly, is a legitimate and useful output. It is
better than forcing a comparison that does not hold and letting it carry weight it cannot
bear.

### Reasons for pessimism, to be tested rather than assumed

- **Duration mismatch.** 1973-74, 1979-80, 1990-91 and the 2022 Russian disruption differ
  greatly in length and in whether the disruption resolved before buffers were tested.
- **No comparable pre-existing glut.** The distinguishing feature of 2026 is that the shock
  hit an expected surplus of 2.4-3.9 mb/d, which supplied roughly a quarter of the
  absorption. No listed historical analogue began from that position, which undermines
  like-for-like comparison of buffer durability specifically.
- **Structural change in the demand side.** EV penetration, electrified rail and the
  petrochemical share of oil demand differ enough that historical demand-response decay rates
  may not transfer.
- **The SPR system itself is different.** IEA collective action did not exist in 1973 and had
  no comparable execution history before 1991.

### Where a comparison might still work

- **Demand response decay.** 1979-80 and 2022 both featured sustained consumer price response
  and conservation policy. How quickly did voluntary conservation fade once prices stabilized?
  This is the single most transferable parameter and directly informs the fragile tier in
  `p2k.3`.
- **Stock rebuild behavior.** How long did countries take to refill emergency stocks after
  previous releases, and at what pace? This bounds how quickly the inventory channel can
  recharge, which matters for a second shock.
- **Rationing thresholds.** At what level of shortfall did governments historically move from
  appeals to mandatory measures? This is a tier-3 trigger indicator for `p2k.3`.

## Acceptance Criteria

- An explicit verdict on whether historical shocks support durability inference, permitted to
  be negative and expected to be partly negative.
- If any parameter does transfer, a stated numerical range plus the reason it transfers.
- Explicit rejection of parameters that do not transfer, with reasons, so future work does
  not reintroduce them.
- No use of historical price responses as a forward price indicator; that is outside epic
  scope by design.

## Source Leads

- Existing comparison work: `data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv` and `docs/hormuz-historical-comparison.md`
- IEA emergency response history and past collective actions
- Academic literature on oil demand elasticity and conservation persistence after 1979

## Work Notes

### Verdict

**Historical shocks do not supply a transferable demand-decay curve, rationing threshold,
bypass exhaustion rate, producer-recovery time or overall absorption mix for 2026.** The
negative result is strong enough that p2k should assign those historical parameters zero
weight rather than use broad historical ranges as if they were uncertainty bands.

Three narrow emergency-stock process parameters do transfer at order-of-magnitude scale:

1. Prior coordinated release programmes were scheduled over **30-180 days**. This is an
   institutional execution-window precedent only; current 2026 observations and contracts
   supersede it for burn rate and remaining volume.
2. IEA emergency-stock obligations were normalised on roughly a **12-18 month** administrative
   horizon after the 2005 and 2022 actions. This supports a slow-recharge flag, not a claim
   that every tank physically returned to its pre-release level in that interval.
3. US direct SPR purchases after 2022 ran at approximately **0.083 mb/d**, with **0.06-0.10
   mb/d** retained as a rounded scheduling band. This is usable only for the order of magnitude
   of US cash-purchase refill, not global stocks, exchange returns, avoided mandated sales or
   net inventory change.

Added `scripts/build_p2k_6_historical_durability_transfer.py` and
`data/derived/hormuz_p2k_6_historical_durability_transfer.csv`. The 13-row artifact identifies
each accepted, context-only and rejected candidate parameter, its integration rule, source,
confidence and prohibited downstream uses. The builder validates all named cases against the
existing 4j7 historical panel. The artifact is registered in `data/manifest.csv`.

### Emergency-stock evidence that partially transfers

| Historical evidence | Defensible number | What transfers | What does not |
|---|---:|---|---|
| 1991 Gulf War contingency plan | 2.5 mb/d | Institutional ability to coordinate quickly. | A stock burn rate: the plan combined stock draw, saving and replacement. |
| 2005 Katrina/Rita | 60 mb over 30 days; stock restoration flexible through 2006 | A 30-day acute programme and year-scale normalisation precedent. | Product mix, country allocation and current usable volume. |
| 2011 Libya | 60 mb over about 30 days | A bridge-to-incremental-supply design precedent. | Grade-specific response or present release ceiling. |
| 2022 Russia actions | 182.7 mb; second 120 mb over six months; obligations restored after 2024Q1 | Six-month execution and roughly 17-month obligation-normalisation precedent. | Present sustainable release rate: 2022 included public and obligated-industry stocks and overlapped the larger US action. |
| US post-2022 direct refill | 43.25 mb scheduled Aug 2023-Dec 2024, about 0.083 mb/d | US purchase/injection order of magnitude. | Global recharge or 2026 exchange-return timing. |

Primary sources:

- IEA 2005 conclusion: https://www.iea.org/news/conclusion-of-iea-collective-action
- IEA 2011 30-day review: https://www.iea.org/news/iea-30-day-review-of-libya-collective-action
- IEA 2022 execution: https://www.iea.org/news/an-update-on-member-countries-contributions-to-iea-collective-actions
- IEA 2022 conclusion/reinstatement: https://www.iea.org/news/iea-governing-board-concludes-2022-collective-actions
- 1991 US activation statement: https://www.presidency.ucsb.edu/documents/statement-press-secretary-fitzwater-the-strategic-petroleum-reserve
- DOE first 2023 purchase: https://www.energy.gov/articles/doe-announces-6-million-barrels-strategic-petroleum-reserve-replenishment
- DOE July 2024 refill tally: https://www.energy.gov/articles/biden-harris-administration-purchases-more-4-million-barrels-strategic-petroleum-reserve

The historical release-rate row (`context-stock-action-market-equivalent-rate`, 0.67-2.5
mb/d) is deliberately **context only**. Its endpoints mix definitions, so p2k.1 must not use
it as a current burn-rate range. The 2026 IEA action is also the largest ever, further weakening
volume extrapolation from the prior sample.

### Rejected demand parameters

No historical episode in 4j7 contains a matched series that isolates temporary conservation
from recession, efficiency investment, vehicle turnover, fuel switching, subsidies and
mandatory policy and then estimates decay after the shock. Therefore:

- **No conservation half-life transfers.** p2k.3 should estimate current persistence from
  current sectors and policies and preserve an unknown field where it cannot.
- **No global rationing threshold transfers.** The 4j7 oil cases span roughly 2-9% gross peak
  loss, but mandatory policy did not order monotonically with that share. Local product
  shortages, distribution failures, price controls, available stocks and politics mattered.
- **The 1970s gasoline elasticity is evidence against transfer.** Hughes, Knittel and Sperling
  estimate US short-run gasoline elasticities of -0.21 to -0.34 in 1975-80 versus only -0.034
  to -0.077 in 2001-06 using comparable specifications. This large structural shift means the
  earlier range must not enter a 2026 global-oil calculation. It is also a price elasticity,
  not a decay parameter. Source: https://www.nber.org/papers/w12530

This task makes **no historical-price-to-future-price inference**. Historical prices are
explicitly rejected as durability parameters.

### Rejected route, supply and balance parameters

- The 1,682-day Tanker War and 2,923-day Suez closure show only that logistics adaptations can
  persist when ships can continue through the attacked route or divert around Africa. Hormuz
  has no Cape-equivalent sea route; a few fixed pipelines and terminals govern oil bypass.
  Those durations do not estimate pipeline throughput decay or failure probability.
- Modern Suez/Red Sea detours add roughly 10-14 days, but that number is physically irrelevant
  to cargo trapped inside the Gulf and is rejected.
- Abqaiq, Katrina and Libya event windows span 16-319 days precisely because their recovery
  mechanisms differ. The spread is not a useful Hormuz reopening range.
- No 4j7 case has a frozen pre-event balance comparable to February 2026's persistent expected
  surplus. The foregone-build absorption share is vintage-specific and remains governed only
  by p2k.5.
- 4j7 severity scores combine exposure, route constraints, inventories, policy and prices.
  They have no physical level, floor, ceiling, burn rate or decay law and must not be ingested
  into p2k.1.

### p2k.1 handoff

Use only these artifact rows as numerical process context:

- `transfer-stock-action-deployment-window`: 30/120/180 days, with current observed execution
  taking precedence.
- `transfer-stock-obligation-normalisation-window`: 12/15/18 months; slow-recharge flag.
- `transfer-us-direct-purchase-refill-pace`: 0.06/0.083/0.10 mb/d; US direct purchases only.

Do not turn any of them into remaining stock volume or a current sustainable burn rate. Treat
`context-stock-action-market-equivalent-rate` as a citation note only. Every row beginning
`reject-` is an explicit prohibition on parameter transfer. Historical work therefore does
not change the 6/12/18-month marginal-absorber arithmetic except to keep emergency-stock
recharge slow and uncertainty high.

### Verification

- `.venv/bin/python scripts/build_p2k_6_historical_durability_transfer.py` wrote 13 rows.
- `.venv/bin/python -m py_compile scripts/build_p2k_6_historical_durability_transfer.py`
  passed.
- All named historical case IDs resolve against
  `data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv`.
- Artifact row IDs and manifest dataset IDs are unique; `git diff --check` passed.
