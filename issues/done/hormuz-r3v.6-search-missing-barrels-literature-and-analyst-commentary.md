---
id: "hormuz-r3v.6"
title: "Search the missing-barrels literature and analyst commentary on the residual"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "residual"
  - "literature"
  - "analyst-evidence"
blocked_by: []
blocks: []
children: []
owner: "r3v6_missing_barrels"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T23:59:00Z"
---

# Search the missing-barrels literature and analyst commentary on the residual

## Description

The project currently characterizes the 308.171 mb implied-versus-observed stock residual as
**exceptional but not unprecedented**: 2.526 mb/d over the March-June frame, exceeding all
six documented annual interagency ranges of 0.30-1.30 mb/d, against a single IEF datapoint
of a still-forecast 4Q23 divergence of 2.6 mb/d.

That benchmark set is thin, and it is doing a lot of work. Two gaps need closing before the
blog can characterize this number confidently.

### Gap 1: the "missing barrels" precedent

There is a well-known historical precedent, generally referred to in the industry as the
**"missing barrels" problem**, in which IEA implied stock builds persistently failed to
reconcile with observed stocks over an extended period in the late 1990s. It generated
substantial analytical debate about whether such gaps represent underestimated demand,
unobserved non-OECD storage, or supply overstatement — which is precisely the question this
project faces.

**This is a lead recalled from general knowledge, not yet verified against a source.** It
must be confirmed or discarded on evidence. If it holds up, it is by far the best available
anchor for whether a 2.5 mb/d discrepancy is shocking or familiar, and would let the project
replace "exceptional" with a genuinely calibrated statement.

### Gap 2: contemporary analyst commentary

The project holds exactly one relevant analyst quote: Kpler noting that a deficit not visible
in the data could be underground draw or further refinery-run cuts, especially in China. One
quote is too thin a basis for the claim that nobody has explained the residual. Search
systematically for whether IEA, EIA, OPEC, IEF, Kpler, Vortexa, Energy Aspects, Rystad,
Argus, S&P Global or academic commentators have addressed the 2026 balance discrepancy
directly.

## The structural argument to test: same-agency pairings nearly close

**Superseded by `hormuz-r3v.7`.** The 261.36 mb input below is not an IEA total-oil
balance, so the pairings in this section are retained only as a record of the hypothesis
that prompted the follow-up. They are not evidence of same-agency closure.

The strongest internal evidence points away from hidden barrels, and it is already sitting in
`data/derived/hormuz_r3v_4_third_source_balance.csv` without being surfaced in any document.

Pairing each agency balance against the IEA observed-stock vintages:

| Pairing | Gap | Per day over 122 days |
|---|---:|---:|
| IEA implied 261.36 vs IEA observed low 258.6 | **2.76 mb** | **0.02 mb/d** |
| IEA implied 261.36 vs IEA observed base 298.0 | 36.64 mb | 0.30 mb/d |
| IEA implied 261.36 vs IEA observed high 368.0 | 106.64 mb | 0.87 mb/d |
| EIA implied 606.17 vs IEA observed base 298.0 | 308.17 mb | 2.53 mb/d |
| OPEC implied 672.30 vs IEA observed low 258.6 | 413.70 mb | 3.39 mb/d |

**Retired inference:** the purported IEA balance reconciles with the IEA observations to within 0.02-0.87 mb/d
across every vintage pairing** — entirely ordinary against the documented 0.30-1.30 mb/d
annual interagency benchmark range. The headline 2.53 mb/d "exceptional" gap appears **only**
when EIA's balance is paired with IEA's tank observations.

This reframes the residual substantially. It is much less "the world cannot locate 308 mb of
oil" and much more "EIA's supply and demand estimates for this period differ from IEA's, and
the project headline crosses agencies." Within a single consistent system the books nearly
close, which is what one would expect if the gap were estimation error rather than several
hundred million barrels of physically unobserved storage.

**Two caveats that must be preserved.** The IEA implied figure of 261.36 mb is a *project
reconstruction* from public fragments, explicitly flagged in the source CSV as not
presentable as the subscriber balance table or as fully same-vintage monthly production. And
agency balances share underlying country submissions, so they are not statistically
independent and cannot be treated as independent draws on a true value.

This argument was checked and rejected; use r3v.7's matched Q2 decomposition instead.

### Consequence for the project headline

This proposal did not survive r3v.7 review. The 3-414 mb range is retired; retaining EIA's
balance and varying only the public observed-stock vintage gives 238-348 mb around the
308.171 mb base. The durable framing is still that this is a model/observation discrepancy,
not "308 million barrels physically unaccounted for."

## Candidate physical mechanisms to weigh, in rough order of strength

1. **Understated demand reduction.** If actual global consumption was below EIA's July
   estimate, the implied draw shrinks with no hidden barrels required. Non-OECD demand is
   estimated as apparent consumption, which is exactly where this error lives. This is the
   leading candidate and notably is *not* a hidden cushioning mechanism — it is the shock
   being partly absorbed by demand nobody measured.
2. **Gulf producer stocks.** The Gulf added roughly 120 mb to storage in March, 100 mb
   floating and 20 mb onshore, and drew it down later. Producer-held inventory is poorly
   covered by all reporting systems.
3. **Non-OECD commercial and refinery tanks outside China**, including India, Southeast Asia
   and entrepot storage at Singapore and Fujairah.
4. **Oil-on-water measurement error.** The June swing of 117 mb in a single month indicates
   very large error bars on this series.

The China government-SPR hypothesis is treated as largely closed by `hormuz-s49.3` and should
not be reopened without new evidence.

## Acceptance Criteria

- The missing-barrels precedent confirmed with citations or explicitly discarded as
  unverifiable.
- If confirmed, the magnitude and duration of that historical discrepancy compared like-for-
  like with the current 2.526 mb/d, and the resolution of that debate summarized.
- A systematic search for contemporary analyst commentary on the 2026 discrepancy, with the
  negative result recorded explicitly if little exists.
- The agency-scatter argument either corroborated or refuted against external sources.
- A revised, defensible characterization of the residual to replace "exceptional, not
  unprecedented," with the candidate mechanisms ranked and the reasoning stated.

## Source Leads

- IEF joint agency comparison work: https://www.ief.org/
- IEA Oil Market Report glossary and miscellaneous-to-balance methodology
- Academic and trade literature on oil market balance discrepancies and non-OECD stock coverage
- `data/derived/hormuz_m8q_11_inventory_residual_scenarios.csv` and `hormuz_r3v_4_third_source_balance.csv`

## Work Notes

- 2026-08-06 correction from `hormuz-r3v.7`: retire the structural claim below that an IEA
  same-agency pairing nearly closes. The 261.36 mb input is not an IEA total-oil balance;
  it is a cross-scope project reconstruction. The historical literature findings remain,
  but this particular 2026 mechanism discriminator does not.

- 2026-08-06: Claimed for a dedicated historical-precedent and public-commentary audit.
  Built `scripts/build_r3v_6_missing_barrels_evidence.py`, which writes the 34-row,
  16-column `data/derived/hormuz_r3v_6_missing_barrels_evidence.csv`. The builder contains
  reproducible calendar arithmetic, contemporary search-audit rows (including negative
  findings), a qualified test of the agency-scatter inference, and an evidence-ranked
  mechanism table. No new package was required.

### Revised verdict

Replace **"exceptional, not unprecedented"** with:

> **A large, historically legible preliminary-balance discrepancy, but not a normal one and
> not evidence that 308 million physical barrels are hidden.** The base rate of 2.526 mb/d
> exceeds the best documented historical episodes found. Comparable cumulative gaps have
> occurred only over longer windows. Keep the roughly 0/310/415 mb epistemic range and expect
> it to move as supply, demand and stock vintages mature.

The late-1990s lead is confirmed, but it does **not** establish that a 300 mb residual over
four months is ordinary:

| episode | sign | rate | cumulative | comparison with March-June 2026 |
|---|---|---:|---:|---|
| 1998 Q1 | implied build not observed | 1.9 mb/d | 171.0 mb | current rate is 32.9% larger |
| 1998 Q2 | implied build not observed | 1.7 mb/d | 154.7 mb | current rate is 48.6% larger |
| 1998 H1 | implied build not observed | 1.799 mb/d | 325.7 mb | similar total only because H1 is six months; current rate is 40.4% larger |
| 1998 full year | implied build not observed | 1.2 mb/d | 438 mb | current produces 70.4% of the annual total in four months |
| 2003 Mar-Jun | observed build exceeded implied build | about 1.6 mb/d | not safely recoverable from the article | same sign; current is 57.9% larger |
| 2003 Q3 | observed build despite implied draw | just over 1.7 mb/d | about a quarter | same sign; current is about 48.6% larger |
| **2026 Mar-Jun** | **implied draw not observed** | **2.526 mb/d** | **308.171 mb** | base cross-system diagnostic |

The sign matters. The famous 1998 episode was a **positive** missing-barrels problem:
supply appeared to exceed demand without a matching reported stock build. The 2026 base is
the reverse: demand appears to exceed supply by more than the reported stock draw. The 2003
Iraq-war dislocation is therefore a closer directional precedent, though its rate was also
smaller.

### What resolved the 1998 debate

There was no single discovery of a 438 mb stockpile:

1. The May 1999 GAO audit, based on IEA data and interviews with IEA and market participants,
   found **both** statistical limitations and actual stocks outside IEA coverage. It said the
   split could not be quantified. IEA then covered OECD primary stocks but no non-OECD tanks;
   independent OECD storage, floating/transit estimates and preliminary supply/demand inputs
   were all incomplete.
2. Later data revisions removed a material part. In August 2001, IEA raised 1999 non-OECD
   demand by 383 kb/d across the FSU, Indonesia, Brazil, Algeria, the Philippines, Iraq and
   Singapore. This reduced 2000 miscellaneous-to-balance from 0.8 to 0.5 mb/d. IEA cited
   unreported petrochemical feedstocks, unrecognized refineries and direct burn.
3. By 2004, Energy Intelligence reported that five years of upward demand revisions and
   smaller downward supply revisions had removed **some, but not all**, of the 1998 gap.
4. IEEJ's 2002 review argued that backwardation and the 1999 tightening likely drew down
   portions of inventory accumulated during 1998, but it also retained statistical error,
   missing non-OECD/secondary stocks and stock incentives as simultaneous causes. This was an
   interpretation, not an ownership-level physical reconciliation.

OPEC's September 2004 methodology note independently describes the structure: the balance is
a small residual between large uncertain supply and demand totals, while non-OECD stocks and
oil on water are weakly measured. It then estimated roughly 0.3 mb/d supply uncertainty and
0.5 mb/d demand uncertainty for that era, but those old values are **not** transplanted into
2026. The peer-reviewed Karbuz (2004) article adds that organizations can publish divergent
country and global totals even when the original administration is the same, due to scope,
classification and conversion choices.

### Contemporary analyst search

The public search covered the organizations named in the issue. It found one direct,
quantified treatment and several useful but non-reconciling balance views:

- **Kpler (direct):** on 13 May it compared its April crude balance deficit of 1.34 mb/d with
  an observed inventory-plus-oil-on-water decline of 0.682 mb/d, leaving **0.659 mb/d**.
  Kpler proposed two alternatives: withdrawals from underground/pipeline systems outside its
  monitoring, or further downward revisions to refinery runs, particularly China. Its
  incomplete-May estimate widened to 1.69 mb/d, with an explicit warning that supply,
  demand and inventory data would be revised. A later Kpler article estimated China's May
  refinery-site stocks down about 15 mb while SPR-classified tanks built about 8 mb; this
  supports commercial flexibility and cuts against a large government-SPR story.
- **Argus (forecast context, not reconciliation):** its April outlook assumed a 4.6 mb/d
  March-June draw, split 2.0 strategic and 2.6 commercial, including 200 mb of the announced
  IEA release. This proves a large draw was a live professional balance assumption, not that
  those barrels were later observed.
- **IEA:** public March-July reports quantify observed stocks, supply response, refinery/end-
  user demand reductions and rerouting, but do not explain the project's EIA-versus-IEA plug.
  Subscriber tables needed for a same-system vintage bridge are not public.
- **EIA:** July estimated 2Q crude draws of 5.1 mb/d and explicitly warns that timely Asian
  demand data, particularly petrochemical HGL use, are limited. It does not reconcile its
  implied inventory series against the IEA stock census.
- **OPEC and IEF:** OPEC supplies a materially different balance; IEF documents the agency
  level differences. Neither publicly reconciles those implications to observed global tanks.
- **Rystad:** public work attributes adjustment to initial buffers and later large refinery-
  run-led demand revisions, and explicitly reported no indication that China drew government
  SPR. No direct residual calculation was found.
- **Energy Aspects:** high-frequency trucking, gasoline and jet indicators found limited
  early consumer response while its inventory work showed draws. This cautions against
  calling every demand revision voluntary conservation, but it does not close a global
  balance identity.
- **Vortexa:** documents pre-positioned Iranian oil on water and delivery/refill lags, but its
  public March scenario is prospective rather than an ex-post residual analysis.
- **S&P Global:** a public 2026 outlook assumed an approximately 3 mb/d full-year inventory
  draw. No observed-versus-implied reconciliation was found.

No separate public 2026 residual explanation was found from academic commentators. That
negative result is informative but bounded: several consultancy balance books and OMR tables
are paywalled, and public searchability is not proof that no internal analysis exists.

### Agency-scatter inference: corroborated, but narrowed

The strong version is too strong. The roughly **411 mb span** across EIA, IEA and OPEC
implied March-June draws proves that the project's 308 mb point is model- and scope-dependent;
all three residuals cannot simultaneously be the same physical stock movement. This is
corroborated by GAO, OPEC, MEES and Karbuz: shared input sources can still yield divergent
balances through revisions, estimation, classification and conversion.

But scatter does **not** prove that hidden physical stocks are small. A shared stock-coverage
blind spot can coexist with different supply/demand errors. GAO reached precisely that mixed
conclusion for 1998 and could not quantify the split. The defensible inference is therefore:

> Measurement/model/vintage error must be material; unobserved physical stock draw may also
> be material, but its share is unidentified.

### Ranked explanations

1. **Cross-system definition/vintage differences plus preliminary supply-demand error — high
   support.** This necessarily explains a material part because the agency balance span is
   larger than the base residual. Public data cannot split supply overstatement from demand
   overstatement.
2. **Understated demand reduction/refinery-run cuts — medium-high support, nested inside #1.**
   EIA itself flags sparse Asian and petrochemical demand data; Kpler repeatedly revised
   Chinese runs down; the historical resolution also moved through upward/downward demand
   revisions. Lower actual use shrinks the implied draw with no hidden barrels.
3. **Unobserved producer, non-OECD commercial, independent, refinery, underground and
   pipeline stocks — medium support.** The category is almost certainly nonzero, and Kpler's
   underground/pipeline hypothesis is plausible. There is no basis to allocate all 308 mb to
   it.
4. **Oil-on-water, transit timing and voyage reclassification — medium support for monthly
   swings, weaker as a complete four-month story.** The June 117 mb swing shows the scale,
   but the project comparator already includes oil on water.
5. **Large China government-SPR draw — low support.** Do not reopen as a base mechanism.
   Commercial/refinery draws are supported; a small opaque government contribution remains
   impossible to rule out.

### Source breadcrumbs

- GAO audit of the 1998 IEA statistics: https://www.gao.gov/assets/rced-99-142.pdf
- IEEJ 2002 historical synthesis: https://eneken.ieej.or.jp/data/en/data/pdf/147.pdf
- OPEC September 2004 methodology note: https://www.opec.org/opec_web/static_files_project/media/downloads/publications/MOMR_092004.pdf
- Oil & Gas Journal on IEA's 2001 demand revisions: https://www.ogj.com/general-interest/companies/article/17220608/ogj-newsletter
- Energy Intelligence retrospective: https://www.energyintel.com/0000017b-a7a3-de4c-a17b-e7e3fd500000
- Karbuz, *Energy Policy* 32(1), 2004: https://doi.org/10.1016/S0301-4215(02)00249-5
- MEES data-revision archive audit: https://www.mees.com/2016/9/23/op-ed-documents/oil-data-is-it-becoming-more-reliable/e5ec96b0-4932-11e7-ae2a-937ac3c1f2e9
- Kpler 13 May residual analysis: https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2
- Kpler later adjustment accounting: https://www.kpler.com/blog/why-a-20-mbd-supply-shock-is-no-longer-moving-oil-prices
- Argus April outlook: https://www.argusmedia.com/-/media/project/argusmedia/mainsite/english/documents-and-files/sample-reports/argus-oil-fundamentals-outlook.pdf

### Validation

- Builder runs with `.venv/bin/python`, compiles, and deterministically regenerates the CSV.
- Output contains 34 unique row IDs and 16 uniform columns.
- Calendar checks reproduce 1998 H1 at 325.7 mb and the current rate at 2.525992 mb/d.
- China government-SPR remains explicitly ranked low-support; no new government-release
  barrel estimate is introduced.
