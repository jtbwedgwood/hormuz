# What happened to the Hormuz barrels, and how much of it do we actually know?

**Research status:** August-vintage synthesis through 18 August 2026. Oil only. No price forecast.

This document answers three questions directly: where the barrels went, how confident we
are in each answer, and whether China quietly cushioned the shock. It sits on top of the
existing reconstruction in `hormuz-historical-oil-accounting-march-july-2026.md` and
`hormuz-inventory-and-demand-residual-stories.md`, then adds four audits: period-matched
national stocks, a three-agency balance comparison, an empirical STEO-revision baseline,
and realized prices as low-weight context. The accounting cutoff is the **11 August EIA
STEO** and **12 August IEA OMR**; U.S. weekly stocks run through 7 August. International
past-month EIA values remain preliminary estimates.

The primary historical frame is now **March-July 2026**, because the August STEO treats
July as a past-month estimate and captures the renewed July disruption. The matched
**March-June** frame remains the route-bridge and Sankey frame because no public,
period-matched July route reconstruction exists.

## The short answer

On the primary March-July frame, global supply was **1,589.6 mb below the frozen February
EIA path**. This is a forecast-revision fact, not proof that every revised barrel was caused
by Hormuz. The matched February-August historical benchmark gives a **1,388.7-1,647.2 mb
Hormuz-plausible range**, which is a small-sample attribution bound rather than a confidence
interval [2][3]. The 1,589.6 mb accounting waist clears four ways:

| How the loss was absorbed | mb | Share | Evidence tier |
|---|---:|---:|---|
| Lower consumption | 570.3 | 35.9% | Educated guess |
| Expected inventory build that never happened | 479.2 | 30.1% | Reasonably assumed |
| Observed inventory draw | 410.0 | 25.8% | Direct same-vintage IEA aggregate |
| **Unreconciled balance plug** | **130.0** | **8.2%** | **Unknown** |

The March-June sensitivity also closes on one August vintage: **1,362.3 = 440.4 lower
consumption + 396.1 foregone build + 341.0 observed draw + 184.8 residual**, all in mb.
The updated Sankey uses that frame: about **1,924.6 mb** of expected Hormuz transit did not
happen; **362.1 mb** was preserved by incremental bypass, **79.3 mb** was offset by the
non-Middle-East regional net plus Oman, and **120.9 mb** remains a route/taxonomy/timing
residual before the 1,362.3 mb waist [1][2][3]. It does not manufacture a July route leg.

Two framing points matter more than any single number:

- **Rerouting and SPR are not siblings.** Rerouted barrels stopped the shortage from
  existing; stock draws and demand cuts absorbed the shortage that remained. Putting them
  in one pie double counts. Hence the waist.
- **The unreconciled plug is not a kind of stock draw.** EIA's March-July implied draw of
  540.0 mb is *defined* by its supply-demand balance. The IEA reports a 410 mb observed
  stock draw on its August vintage [4]. The remaining 130 mb is a residual that absorbs
  genuinely unobserved stocks *and* every measurement error in the supply and demand series,
  indistinguishably. It is shown as its own slice, not tucked under inventories.

## How much do we actually know?

Every barrel in the market-clearing bridge is assigned to one of four tiers in
`data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv`:

| Tier | Meaning | mb | Share |
|---|---|---:|---:|
| **T1 Directly observed** | Direct same-vintage reported stock aggregate | **410.0** | **25.8%** |
| **T2 Reasonably assumed** | Exact arithmetic on a frozen forecast counterfactual | **479.2** | **30.1%** |
| **T3 Educated guess** | Exact vintage gap, uncertain causal/mechanism attribution | **570.3** | **35.9%** |
| **T4 Unknown** | Cross-system residual without independent observation | **130.0** | **8.2%** |

Thus the mechanically unknown bucket falls from the July-vintage headline's **422.3 mb
(29.3%)** to **184.8 mb (13.6%)** on the like-for-like March-June frame, a decline of
**237.5 mb and 15.7 percentage points**. On the recommended March-July frame it is
**130.0 mb (8.2%)**. The former 117-528 mb range is retired: it mixed balance models and
stock vintages rather than bounding the August bridge. Public August OMR tables do not
expose the Q2/Q3 supply and demand levels needed to construct a new same-vintage model
range, so publishing a narrower numeric interval would create false precision. The ledger
therefore reports the exact cross-system plug and labels its physical interpretation low
confidence.

Three caveats on the tally:

1. **The aggregate upgrade is real; national rows remain nested.** The IEA now publishes a
   same-vintage 341 mb March-June and 410 mb March-July observed draw. Japan's exact June
   quantities imply a **71.641 mb** net draw; with usable Austria, Belgium and Finland
   endpoints, the new national T1 subset is **70.782 mb**. Those country changes are already
   inside the IEA aggregate and are not added to it [17][18].
2. **The IEA aggregate is solid; the country split is not.** The ~290 mb collective
   emergency release delivered through 21 July is a reported aggregate [8]. Beyond the U.S.,
   Japan and Italy, the country allocation is pro-rated from the 19 March plan at a common
   0.688 execution factor [9] — arithmetic, not observation.
3. **The demand mechanism split is still not causally identified.** This refresh does not
   book a second arbitrary T4 allowance inside the demand slice. The entire consumption
   vintage gap remains T3: exact arithmetic, uncertain causal composition. Regional and
   country demand detail is being refreshed separately and must not be mixed into this bridge.

## Why the "model discrepancy" is so large — and why that is not a dodge

Your instinct that too much is attributed to model discrepancy is half right, and the half
that is wrong is the more important half.

The existence of a residual is **legitimate and expected**. Real-time global oil balances never
reconcile. The IEA's own methodology says an exact supply-demand-stock balance cannot be
achieved, and its `miscellaneous to balance` item explicitly combines non-reported stocks,
floating storage and oil in transit, *plus errors in the supply, demand and stock estimates*
[5]. That is almost a word-for-word description of the residual. The August result changes
the historical claim materially. The **184.786 mb March-June plug is 1.515 mb/d**: still
above the documented 0.30-1.30 mb/d annual interagency range, but below the 1998 H1
1.799 mb/d benchmark. The primary **130.013 mb March-July plug is 0.850 mb/d**, inside that
historical range and far below the old 2.526 mb/d rate. The draft should no longer say the
primary-frame discrepancy is "outside the usual range." It is a normal-sized preliminary
balance discrepancy by this bounded comparison, not 130 mb of measured hidden barrels.

The three-way comparison initially appeared to change what the number meant, but a follow-up
scope audit found that the apparent **261.4 mb IEA March-June draw was not a valid total-oil
balance**. It subtracted successive-vintage monthly OPEC+ crude production from a quarterly
call-on-DoC number, then treated the result as if it were global demand minus total supply.
That cross-scope point—and the near-zero residual obtained by pairing it with IEA observed
stocks—are retired [20].

What could be decomposed cleanly on the **July vintage** was Q2. Calendar-weighted EIA inputs imply a
5.094 mb/d draw, while public IEA demand and monthly supply imply 2.985 mb/d: a **2.110 mb/d
difference**. Lower IEA demand accounts for **1.254 mb/d (59%)** and higher IEA supply for
**0.856 mb/d (41%)**. The IEF's comparable supply table places 0.8 mb/d of the latter in
non-DoC supply plus DoC NGLs, leaving only **0.056 mb/d**, well within rounding, for the rest.
That is evidence *against* the attractive story that the IEA gap mainly reflects more Gulf
bypass credit. A precise March-June split remains unavailable because the revised monthly
IEA March demand level is subscriber-only. Transparent March-demand anchors produce an IEA
draw of roughly **300-495 mb** and an EIA-minus-IEA model gap of roughly **111-307 mb**; these
remain July-vintage sensitivities, not hidden stocks or a confidence interval. The public
August OMR omits Q2/Q3 supply and demand levels, so neither Q2 nor Q3 can be recomputed on a
single August vintage. Pairing August EIA levels with July IEA levels would be mislabeled.
OPEC's 672.3 mb quarterly
proxy remains useful as a scope diagnostic, but its 304 mb demand difference is coincidental:
OPEC's comparable outside-DoC supply is **1.2 mb/d lower**, not about 3 mb/d higher, than EIA's.

Two presentation defects are now fixed:

- **Model error was effectively booked twice.** The implied draw already contains all
  balance error; the former residual scenario then assigned another ~123 mb of the old 308 mb to "EIA
  supply, demand, taxonomy and balance error." Splitting observed from plug at the top level,
  as done here, removes the double booking.
- **The 298 mb mixed-vintage comparator is retired.** The August OMR's same-vintage aggregate
  is 341 mb through June and 410 mb through July [4]. Public March-June monthly cells remain
  subscriber-only, so no false monthly August series is fabricated.

The oil-on-water audit corrects a tempting but invalid shortcut. Global oil on water **fell
117 mb in March**; the +100 mb previously used as a global build was actually Gulf floating
storage nested inside that decline. With May oil on water bounded at ±35 mb, onshore-
accessible stocks drew **316 / 351 / 386 mb** through June. Substituting those figures for
the former 298 mb appears to shrink the old residual by 18 / 53 / 88 mb, but this is a boundary mismatch:
EIA's implied draw and IEA's observed total both include in-transit oil. Reclassifying only
the observed side closes **zero barrels** on a matched boundary. The real implication is
about accessibility and durability, not accounting closure. Public August evidence adds a
63 mb July oil-on-water draw but still does not expose the March-June monthly split.

The counterfactual problem is now bounded rather than merely acknowledged. The entire
reconstruction now rests on "frozen February STEO vs August STEO" [2][3], which captures
**everything that changed EIA's mind since February** — Hormuz, ordinary demand marks,
taxonomy changes, and unrelated events such as Russia-Ukraine refinery damage. Across
February-to-August vintage pairs in 2017-19 and 2023-25, after removing Russia from both the
target and baseline, the preferred signed p10-p90 bands imply a Hormuz-plausible
March-June supply loss of **1,220-1,419 mb**; the March-July range is **1,389-1,647 mb** [21].
These are plausibility bands, not identified treatment effects, but ordinary revision is far
too small to explain the shock: the 2026 supply revision is roughly an order of magnitude
larger than the largest prior downward revision in the six-year reference sample. Asia and
Oceania plus the Middle East account for about 500 mb of the March-July demand revision and
both lie far outside every reference-year result. A band endpoint can exceed the observed
revision because signed ordinary revision sometimes would have raised supply or demand,
partly offsetting the shock rather than adding to the downward mark.

## The China question

**The strong claim — that a coordinated Chinese SPR drawdown was key to cushioning the
global shock — is not supported by the public evidence, and the visible data cut against it.**
This repo already reached that conclusion independently in `hormuz-s49.3`, which scored
confidence in a large government-SPR release at roughly 20/100.

What the evidence shows:

- China was **building** stocks going into and through the early shock. EIA estimates China
  added ~1.1 mb/d to strategic inventories in 2025, reaching ~1.4 bn bbl by December, and
  says preliminary data indicate continued builds into 2026 before the conflict [10]. The
  IEA reported China adding 40 mb to tanks in March 2026 *while global stocks were falling*
  [14], and Kpler put visible Chinese crude near a record 1.24 bn bbl in mid-May, up ~25 mb
  since the war began [13].
- The later draw is **modest and commercial**. Energy Aspects, citing Kayrros, estimated
  almost 25 mb drawn from May through 7 June [11]. Bloomberg's reporting explicitly
  describes these as commercial reserves, separate from the strategic petroleum reserve [12].
- The apparent **88 mb May draw does not survive a like-for-like official balance**. Customs
  recorded 33.08 Mt of total crude imports (7.79 mb/d), while NBS recorded 18.57 Mt of
  domestic output and 53.72 Mt of processing. At 7.3 bbl/t, that implies a **15.1 mb May
  draw** (about 10.3-19.9 mb if the import conversion alone varies by +/-2%). Substituting
  the 6.36 mb/d seaborne series creates a 59.4 mb draw because it omits 1.43 mb/d of
  pipeline supply and/or tanker-tracking differences; pairing that seaborne number with a
  separate 13.5 mb/d run estimate creates the larger 88 mb residual. The official-total
  balance also gets the observed signs right in March and June, while the seaborne balance
  incorrectly implies an April draw [24].
- The widely quoted "~1 mb/d of reserve use" figures are **authorization and analyst
  capacity, not observed delivery** [11]. Our ledger flags them as context only and excludes
  them from the arithmetic.
- A hidden underground transfer **cannot be ruled out** — Kpler says so directly [13] — but
  that is "we cannot see," not "we saw it." Our base scenario assigns just 20 mb to hidden
  Chinese government draw, with a 75 mb high case. Those scenarios are not added to the
  1,589.6 mb March-July accounting waist.

So why do the videos seem well-researched? Because they are probably fusing several true
facts into a tidier causal story than the data support. Three specific traps:

1. **A definitional trap.** EIA deliberately reports China's government-held *and*
   NOC-commercial stocks together as "strategic oil inventories," because Beijing directs
   NOCs to hold emergency oil commercially. So "China has 1.4 bn bbl of strategic
   inventories" is **not** "China has 1.4 bn bbl in a government SPR" — EIA separately puts
   the government-held portion near 360 mb [10].
2. **A mechanism substitution.** China's real contribution to easing the global balance was
   overwhelmingly **demand-side, not supply-side**: crude-processing shortfalls of roughly
   25 / 39 / 81 mb year over year in April, May and June, plus lower imports, refinery-run
   cuts and refined-product export controls [16][11]. That genuinely eased world balances —
   but by *consuming and importing less*, which is close to the opposite of releasing
   reserves to supply others.
3. **A visibility trap.** China holds real optionality that is invisible in Western data:
   bonded Iranian barrels, floating storage, and origin relabeling via Malaysia and Indonesia
   [15]. Analysts saying "we cannot verify" gets compressed into "it is happening."

**Verdict:** I would not call the videos propaganda. Their underlying facts — a huge Chinese
stockpile, aggressive discounted buying, hard run cuts — are largely correct and their
conclusion that China cushioned the shock is *directionally* right. The specific causal
mechanism they assert, releasing strategic stocks to supply the world, has no measured public
support. Two honest caveats in the other direction: absence of evidence is doing real work
here, since China publishes no clean SPR series, and the one place a large draw could hide is
exactly the residual nobody can physically classify. But the early data showing Chinese tanks *building* is
genuine evidence against, not just silence.

## What the follow-up audits changed, and what remains

The four `hormuz-r3v.2` to `.5` tasks are now complete.

1. **National stocks:** Japan's exact June endpoint lifts the usable national subset to a
   70.782 mb net draw after the three usable Eurostat countries. It remains nested inside
   the IEA global stock aggregate.
2. **Third balance:** the August same-vintage stock aggregate cuts the plug to 184.8 mb
   through June and 130.0 mb through July. The exact July-vintage Q2 agency split remains
   59% demand-side and 41% supply-side, but no August Q2/Q3 replication is possible from
   public levels.
3. **Ordinary revision:** the 1,589.6 mb primary headline is explicitly a revision-path fact;
   the preferred Hormuz-plausible supply band is 1,389-1,647 mb through July. The six-year sample
   is small and eventful, so expanding the vintage benchmark would improve tails more than
   it would change the central story.
4. **Prices:** Brent averaged $103 in March and $117 in April, peaked at $138 on 7 April,
   and fell to $69.56 on 6 July during the fragile reopening. The July re-closure did **not**
   produce a near-non-response: Brent reached $76.50 on 8 July and $105.32 on 23 July,
   before easing to $93.26 on the latest official spot observation, 11 August. WTI rose from
   $69.60 on 6 July to $93.08 on 23 July and ended its official spot series at $84.77 on
   11 August [22]. This is chronology, not causal identification: security news, reopening
   expectations, policy, macro demand, unrelated supply and positioning moved concurrently,
   and no price-to-barrels inference enters the accounting. The curve is more useful for the
   narrower storage question: WTI front-minus-December was backwardated on all 84
   March-June observations and Brent on 82 of 84; both were backwardated on every observed
   session from 8 July through the latest completed 17 August session. That weighs against
   profit-seeking carry storage while leaving blocked cargoes, congestion, sanctioned dwell
   and voyage float live [23]. U.S. regular gasoline was $4.049/gal and on-highway diesel
   $5.454/gal on 17 August, about 42% and 51% above their January-February means; elevated
   retail prices alone do not establish U.S. demand destruction.

## Sources

1. IEA, *How global oil supplies have readjusted to help fill the huge gap left by the Strait of Hormuz shock* — https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
2. EIA, *Short-Term Energy Outlook*, February 2026 workbook (frozen baseline) — https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
3. EIA, *Short-Term Energy Outlook*, August 2026 workbook and report — https://www.eia.gov/outlooks/steo/archives/aug26_base.xlsx, https://www.eia.gov/outlooks/steo/archives/aug26.pdf
4. IEA, *Oil Market Report*, August 2026 — https://www.iea.org/reports/oil-market-report-august-2026
5. IEA, *Oil Market Report glossary and methodology* (stocks, miscellaneous to balance) — https://www.iea.org/articles/oil-market-report-glossary
6. EIA, weekly U.S. Strategic Petroleum Reserve stocks — https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
7. EIA, weekly U.S. total commercial petroleum stocks — https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1
8. IEA, *Executive Director statement on oil markets*, 21 July 2026 (≈290 mb delivered) — https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
9. IEA, *Member country contributions to collective action*, 19 March 2026 — https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
10. EIA, *Today in Energy*: China's strategic and commercial oil inventories, 12 May 2026 — https://www.eia.gov/todayinenergy/detail.php?id=67504
11. Bloomberg via Energy Connects, *China taps commercial oil stockpiles to help weather Gulf shock*, 10 June 2026 — https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
12. Bloomberg via The Straits Times, *China allows state oil firms to tap reserves* (commercial volumes distinct from SPR) — https://www.straitstimes.com/asia/china-allows-state-oil-firms-to-tap-reserves-as-middle-east-war-drags
13. Kpler, *Drawing down: how the market is absorbing the Hormuz shock*, 13 May 2026 — https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2
14. IEA, *Oil Market Report*, April 2026 (China +40 mb March build; Middle East floating storage) — https://www.iea.org/reports/oil-market-report-april-2026
15. CGEP / Erica Downs, *Where China gets its oil: 2025 crude imports reveal stockpiling* — https://www.energypolicy.columbia.edu/where-china-gets-its-oil-crude-imports-in-2025-reveal-stockpiling-and-changing-fortunes-of-certain-suppliers-including-those-sanctioned/
16. China National Bureau of Statistics, energy production releases for April, May and June 2026 — https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html, https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html, https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html
17. Eurostat, monthly emergency oil stocks (`nrg_stk_oilm`) — https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_stk_oilm
18. Japan METI, February and June 2026 petroleum-reserve quantities — https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260415oil.pdf, https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260817oil.pdf
19. Yonhap, South Korean deputy-minister statement on release timing, 26 May 2026 — https://en.yna.co.kr/view/AEN20260526010800320
20. IEF, July 2026 comparative analysis of IEA/OPEC/EIA monthly reports; OPEC July MOMR — https://www.ief.org/_resources/files/news/comparative-analysis-of-monthly-reports-on-the-oil-market/july-2026/ief-comparative-analysis-07-2026.pdf, https://www.opec.org/assets/assetdb/momr-july-2026.pdf
21. EIA, STEO archive workbooks used for the 2017-19 and 2023-26 vintage-pair benchmark — https://www.eia.gov/outlooks/steo/archives/
22. EIA via FRED, daily Brent and WTI spot prices; EIA weekly U.S. retail fuel prices — https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU,DCOILWTICO, https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm
23. CME, March backwardation commentary and 5 August energy bulletin — https://www.cmegroup.com/newsletters/fresh-from-the-trading-room/2026-03-23.html, https://www.cmegroup.com/daily_bulletin/current/Section61_Energy_Futures_Products.pdf
24. China crude-balance inputs: EIA synthesis of GAC monthly imports; NBS monthly energy
    releases; Reuters/Kpler/Vortexa reported seaborne figures — https://www.eia.gov/todayinenergy/detail.php?id=67905, https://www.stats.gov.cn/english/PressRelease/, https://www.hydrocarbonprocessing.com/news/2026/06/chinas-crude-oil-imports-slump-but-its-economics-not-altruism/, https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d, https://www.brecorder.com/news/amp/40433885

## Artifacts

- `data/derived/hormuz_a4d_6_august_absorption_bridge.csv` — both August-vintage market
  bridges, the matched route bridge, residual benchmarks and public-source limitations
- `data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv` — tier assignment for both frames
- `figures/fig-r3v-hormuz-absorption-sankey.svg` and `-data.csv` — the waist-node Sankey
- `scripts/build_r3v_1_confidence_tiered_absorption.py` — reproduces both
- `data/derived/hormuz_r3v_2_period_matched_national_stocks.csv` — national stock endpoint audit
- `data/derived/hormuz_r3v_3_price_context_summary.csv` — realized-price context only
- `data/derived/hormuz_r3v_3_time_spread_summary.csv` — medium-weight storage-regime discriminator
- `data/derived/hormuz_a4d_9_product_retail_price_summary.csv` — EIA U.S. product,
  retail-price and gross-crack-proxy context with explicit margin caveats
- `data/derived/hormuz_r3v_4_third_source_balance.csv` — three-agency balance and residual benchmark
- `data/derived/hormuz_r3v_5_ordinary_steo_revision_baseline.csv` — ordinary-revision baseline and causal-plausibility bands
- `data/derived/hormuz_r3v_6_missing_barrels_evidence.csv` — historical precedent and mechanism ranking
- `data/derived/hormuz_r3v_7_interagency_balance_decomposition.csv` — matched-Q2 agency-gap
  decomposition, March sensitivity and scope guardrails
- `data/derived/hormuz_p2k_12_oil_on_water_split.csv` — onshore-accessibility and boundary test
- `data/derived/hormuz_p2k_13_rerouting_causal_test.csv` — rerouting, refill and competing-mechanism bounds
- `data/derived/hormuz_g7t_1_china_crude_balance.csv` — February-July customs-total versus
  seaborne China crude balance, observed-stock sign checks and conversion sensitivity
- `scripts/build_g7t_1_china_crude_balance.py` — reproduces the China balance
