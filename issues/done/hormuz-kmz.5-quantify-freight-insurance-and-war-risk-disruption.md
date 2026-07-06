---
id: "hormuz-kmz.5"
title: "Quantify freight, insurance, and war-risk disruption"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "freight"
  - "insurance"
  - "supply"
blocked_by:
  - "hormuz-fyp.2"
blocks:
  - "hormuz-kmz.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:38Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Quantify freight, insurance, and war-risk disruption

## Description

Estimate how freight rates, war-risk premia, tanker availability, and rerouting delays affect delivered supply and prices even when physical cargo is not fully blocked.

## Acceptance Criteria

Evidence covers rate changes, insurance quotes or reports, voyage delays, vessel availability, and likely pass-through.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-fyp.2` - Build canonical disruption chronology
- Blocks: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.

### Research pass: 2026-07-05

Scope: freight, war-risk insurance, tanker availability, traffic recovery, and likely delivered-price pass-through in the 2026 Hormuz disruption / partial-recovery window. I used current/lately published material dated March 4 through July 1, 2026, with a few July 5 summaries for the latest traffic narrative.

#### Evidence table

| metric | observed_change_or_level | period/date | affected_segment | mechanism | source | confidence | notes |
|---|---:|---|---|---|---|---|---|
| Additional war-risk premium (AWRP), Persian Gulf | Rose to around 2.5% of hull value per 7-day period in early March, then eased to close to 1% by March 27; some transits paid around 0.8% after no-claims bonus | Early March 2026; Mar. 27, 2026 | Tankers transiting Hormuz / Gulf | War-peril repricing after attacks and perceived closure | [S&P Global, Mar. 30, 2026](https://www.spglobal.com/energy/en/news-research/latest-news/shipping/033026-war-risk-insurance-cost-off-highs-but-still-elevated-in-persian-gulf) | High | This is the cleanest numeric insurance series I found. Pre-war level was about 0.1%-0.15%, so even the March 27 rate was still roughly 8x-10x normal. |
| Peak war-risk quote on some stranded cargoes | Up to 10% of H&M value in mid-March; one crude-laden Suezmax quote was $7.5m, above the $6.5m freight to destination | Mid-March 2026 | Stranded crude cargoes / Suezmax voyages | Extreme scarcity of cover and elevated perceived vessel/crew risk | [S&P Global, Mar. 30, 2026](https://www.spglobal.com/energy/en/news-research/latest-news/shipping/033026-war-risk-insurance-cost-off-highs-but-still-elevated-in-persian-gulf) | High | This is the strongest evidence that insurance alone could exceed the freight component during the peak. |
| Insurance availability vs crew-risk constraint | War insurance remained available; P&I remained available; some charterer P&I covers were cancelled/repriced; owners cited crew safety as the reason not to transit | Mar. 30, 2026 | Shipowners / charterers | Operational risk and crew refusal, not just insurance absence | [LMA / Lloyd’s, Apr. 2026](https://lmalloyds.com/safety-concerns-not-insurance-availability-driving-reduced-vessel-traffic-in-the-strait-of-hormuz/) | High | Important for interpretation: cover availability improved before traffic normalized, so behavior was driven by human-risk and corporate-policy constraints too. |
| Middle East-to-Asia VLCC freight | VLCC rates from the Middle East to Asia hit the highest since at least Nov. 2005 in March; EIA says March 2026 rates were at a multi-decade high | Mar. 26, 2026 | Crude tankers / Asia-bound flows | Backlog inside Gulf, fewer available hulls, war-risk costs, longer/safer routing | [EIA, Mar. 26, 2026](https://www.eia.gov/todayinenergy/detail.php?id=67386) | High | EIA ties the freight spike directly to the closure and to reduced global tanker availability. |
| VLCC spot freight benchmark | TD3 rose to W419, or $423,736/day; rate doubled from Friday | Mar. 4, 2026 | VLCCs moving Middle East crude to China | Emergency closure plus insurance and route disruption | [Reuters via Journal Record, Mar. 4, 2026](https://journalrecord.com/2026/03/04/middle-east-oil-lng-shipping-costs-strait-hormuz/) | High | This is the clearest concrete day-rate quote at the crisis peak. |
| LNG tanker freight | Atlantic LNG rates rose 43% to $61,500/day; Pacific rates rose 45% to $41,000/day; spot LNG shipping could exceed $100,000/day | Mar. 4, 2026 | LNG carriers / Qatar and regional gas flows | Tight vessel availability and closure fears | [Reuters via Journal Record, Mar. 4, 2026](https://journalrecord.com/2026/03/04/middle-east-oil-lng-shipping-costs-strait-hormuz/) | High | Shows the disruption was not only crude-oil-specific. |
| Current tanker hire cost after partial recovery | Hiring a tanker outside Hormuz jumped to $190,500/day from $106,500 a week earlier; VLCC daily earnings inside the Gulf rose to nearly $470,000/day | Jun. 23, 2026 | Tankers staging for Gulf loadings | Expected rebound in Middle East exports, still-tight capacity | [Reuters via Dawn, Jun. 24, 2026](https://www.dawn.com/news/2010304) | High | The freight market remained very hot even as traffic began to return. |
| Current war-risk level after easing | War-risk costs softened to around 3% of ship value from around 5% over the prior week | Jun. 23, 2026 | Tankers transiting the Gulf / Hormuz | Gradual reopening reduced panic pricing, but risk remained elevated | [Reuters via Marinelink, Jun. 23, 2026](https://www.marinelink.com/news/gulf-tanker-rates-nearly-double-middle-540569) | High | That is still roughly 30x the pre-war 0.1% level and implies multi-million-dollar insurance on a $100m hull. |
| Traffic recovery, but still below normal | 55 merchant ships transited on Jun. 20 carrying more than 17m barrels of oil; still well below pre-war norms | Jun. 20, 2026 | Commercial shipping / energy flows | U.S. support and ceasefire reopened the lane, but confidence lagged | [USCENTCOM, Jun. 20, 2026](https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/4522490/commercial-vessels-flow-through-open-strait-of-hormuz/) | High | Good official benchmark for early recovery. |
| Evacuation / queue release pace | 57 ships carrying an estimated 1,100 seafarers transited since Jun. 23 under the UN evacuation scheme | Jun. 25, 2026 | Backlogged vessels / stranded crews | Managed evacuation routing via Omani and Iranian waters | [Reuters via MarineLink, Jun. 25, 2026](https://www.marinelink.com/news/crude-oil-shipments-hormuz-reach-highest-540664) | High | This is the best quantitative read on how much backlog was still being worked down. |
| Route reversals / rerouting | A Panama-flagged crude tanker did a U-turn after trying to transit toward Omani waters; another tanker was ordered to change course and wait for instructions | Jun. 25, 2026 | Individual voyages / routing | Iranian corridor designation and security enforcement | [Reuters via MarineLink, Jun. 25, 2026](https://www.marinelink.com/news/crude-oil-shipments-hormuz-reach-highest-540664) | High | Strong evidence that the disruption was operational, not just price-based. |
| Slowdown after renewed risk | Only 22 crossings on Sunday; 108 vessels from Fri.-Sun. after a weekend of attacks | Jun. 29, 2026 | All vessel classes | Attack shock reduced recovery pace | [WSJ live coverage snippet, Jun. 29, 2026](https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-06-29-2026/card/traffic-slows-at-strait-of-hormuz-after-weekend-of-fighting-efoZI5awgduUBaxvuGP2) | Medium | This is a good short-window measure of fragility, though the source is a live-coverage snippet rather than the full article. |
| Near-standstill after weekend attack | Only three ships crossing on Monday; traffic had ground to a near standstill | Jun. 30, 2026 | Commercial shipping / queue formation | Security shock and delayed restarts | [Reuters via Facebook, Jun. 30, 2026](https://www.facebook.com/Reuters/posts/traffic-through-strait-of-hormuz-slows-after-attack-on-shipclick-the-link-in-the/1590006266323433/) | Medium | Useful as the post-attack nadir in the partial-recovery phase. |
| Backlog size | About 1,000 ships, including roughly 200 oil tankers, were waiting to pass through Hormuz | Late Jun. / early Jul. 2026 | Tanker and non-tanker backlog | Limited safe routing, mines, and administrative control | [Reuters snippet reposted by CNBC Africa, Jul. 2026](https://www.facebook.com/Cnbcafrica/posts/at-least-three-iranian-tankers-carrying-nearly-five-million-barrels-of-crude-oil/1498447562322044/) | Medium | Multiple reposts carried the same figure; I would treat this as a strong directional indicator, not a precise census. |
| Normal traffic still not restored | Full commercial traffic not expected to resume until Iranian-laid naval mines are cleared from key routes | Late Jun. 2026 | Strait-wide flow | Physical hazard + routing governance | [Reuters via Facebook, late Jun. 2026](https://www.facebook.com/Reuters/posts/the-marinetraffic-tracker-showed-vessels-moving-through-the-strait-of-hormuz-aft/1581742440483149/) | Medium | This helps explain why traffic can recover without the market returning to normal. |

#### Working synthesis

- Peak disruption imposed two separate cost layers: freight and war-risk insurance. At the March peak, freight hit a multi-decade high and one quoted Suezmax war-risk premium of $7.5m exceeded the $6.5m freight to destination.
- By late March, war-risk pricing had eased but was still far above normal, and by late June it had softened further to about 3% of hull value. That still leaves insurance as a meaningful delivered-cost component.
- Crew-safety policy and vessel availability remained binding even when cover was technically available. In practice, that meant rates stayed elevated because too few ships were willing or allowed to move.
- The recovery was real but unstable: official traffic was back to 55 merchant ships on June 20, then the market whipsawed to only 22 crossings on June 29 and three ships on June 30 after fresh security incidents.
- For delivered-price pass-through, the most defensible order-of-magnitude estimate is that peak Hormuz disruption added several dollars per barrel to crude delivered costs, and in at least one Suezmax case the insurance premium alone was on the order of the freight bill. A rough inference from the $7.5m insurance quote on a crude-laden Suezmax suggests the all-in landed-cost shock could be around $14/bbl on a ~1m bbl cargo if fully passed through. That estimate is an inference, not a quoted market price.

No data file created.

### Completion Note

- 2026-07-06: Acceptance criteria met for current project stage. Notes cover war-risk premiums, tanker and LNG freight, traffic recovery/slowdown, crew and insurance constraints, and likely delivered-price pass-through. Remaining uncertainty is source refresh, not a blocker for market-balance or master-table use.
