---
id: "hormuz-g7t.1"
title: "Reconcile the monthly China crude balance against customs totals"
type: "task"
status: "done"
priority: "P1"
parent: null
labels:
  - "china"
  - "inventories"
  - "verification"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# Reconcile the monthly China crude balance against customs totals

## Description

Widely circulated June reporting (Reuters/Clyde Russell citing Kpler, syndicated onward)
argues that China drew heavily on its crude stockpile because **seaborne** imports collapsed
far more than refinery runs did. Taken at face value the May figures imply a very large draw,
which appears to contradict this repo's conclusion in `hormuz-s49.3` that no large
government-reserve release is evidenced.

The reported May inputs are seaborne imports of **6.36 mb/d** (down from 8.10 in April and
11.39 in February) against crude processing of **13.5 mb/d**. Subtracting China's own
production of roughly 4.3 mb/d leaves an implied draw of about **2.84 mb/d, or 88 mb in May
alone** — roughly 3.5x the Kayrros/Energy Aspects estimate of ~25 mb for the longer
May-to-7-June window, and the **opposite sign** to Kpler's own observed onshore tank data,
which put Chinese crude near a record 1.24 bn bbl in mid-May, up ~25 mb since the war began.

The suspected explanation is that the implied balance omits supply the seaborne series cannot
see. China imports roughly **1 mb/d by pipeline** (Russian ESPO ~0.8-0.9, Kazakhstan ~0.2,
plus a small and usually underused Myanmar line), none of which touches a tanker. Tanker
tracking also systematically undercounts dark and relabeled cargoes; CGEP puts sanctioned
crude at 2.6+ mb/d in 2025 with heavy Malaysia/Indonesia relabeling, and those flows would go
darker, not lighter, during a war involving Iran. A scratch reconciliation shows that adding
back ~1.1 mb/d of pipeline and ~1.0 mb/d of dark seaborne brings the implied May draw to
about **23 mb**, essentially the Kayrros figure — no hidden reserve release required.

That reconciliation is plausibility arithmetic using approximate pipeline volumes from general
knowledge. **The repo has no China pipeline import series and no customs series.** This task
replaces the guess with data.

**The decisive test is one number.** China's General Administration of Customs publishes
**total** crude imports including pipeline. The gap between the GAC total and the Kpler
seaborne figure is exactly the quantity in dispute, and it comes from a source independent of
tanker tracking.

## Scope

Build a monthly China crude balance for **February through July 2026**, extending to August if
GAC and NBS have published by the time this is picked up. Do not do May alone — the single
month is what made the original claim look decisive, and the shock window has a partial June
reopening and a July re-closure that should show up in the series.

Per month, collect:

1. **GAC total crude imports** (customs, includes pipeline).
2. **Kpler/Vortexa seaborne crude imports** as reported in press coverage, for the same month.
3. **The difference**, reported explicitly as its own column: pipeline plus any tanker-tracking gap.
4. **NBS domestic crude production.**
5. **NBS crude processing / refinery runs.**
6. **Implied stock change** = (2 or 1) + (4) − (5), computed **both** ways so the effect of
   using seaborne instead of total imports is visible per month rather than argued in prose.

Then reconcile the implied series against every observed comparator the repo already holds:

- IEA monthly China observations: **+40 mb build in March**, **−41 mb draw in June**.
- Kpler observed onshore crude: near-record 1.24 bn bbl in mid-May, up ~25 mb since war onset.
- Kayrros/Energy Aspects: ~25 mb drawn May to 7 June; ~1 mb/d prospective rate.
- EIA: ~1.1 mb/d added to strategic inventories through 2025 to ~1.4 bn bbl, continued builds
  into early 2026; commercial crude ~1.0 bn bbl at Dec 2025; government-held portion ~360 mb.

## Acceptance Criteria

- A monthly Feb-Jul (Aug if available) table in `data/derived/` with the six fields above and
  the two implied-stock-change variants side by side.
- An explicit verdict on whether the ~88 mb May draw survives once total imports replace
  seaborne, stated as a number with its remaining uncertainty.
- The implied series compared month by month against the observed comparators, with any
  month where implied and observed disagree in **sign** called out rather than averaged away.
- The tonnes-to-barrels conversion factor stated explicitly, with a sensitivity line. GAC and
  NBS report in tonnes; crude conversion is roughly 7.3 bbl/t but varies by grade, and a 2%
  factor error is ~0.2 mb/d on an 11 mb/d import base — large enough to matter here.
- No attribution of any draw to government versus commercial stock without a published
  ownership bridge. `hormuz-s49.3` scored confidence in a large government-SPR release at
  about 20/100; this task may revise that only on ownership evidence, not on balance
  arithmetic.
- Blog-facing output: either a confirmation that the existing blog-safe China wording stands,
  or replacement wording.

## Dependency Notes

- Blocks: `hormuz-ccx.5` - Draft blog post from evidence package
- Related: `hormuz-s49.3` (China SPR release claims), `hormuz-f6r.2` (China exposure and
  substitution), `hormuz-a4d.8` (China demand mechanism evidence)

## Work Notes

- 2026-08-20 completed. Deliverables are
  `data/derived/hormuz_g7t_1_china_crude_balance.csv`, its reproducible builder
  `scripts/build_g7t_1_china_crude_balance.py`, a manifest entry, and tightened blog-facing
  wording in `docs/hormuz-what-happened-to-the-barrels.md`.
- **May verdict:** the 88 mb implied draw does not survive. GAC total imports were 33.08 Mt
  (7.790 mb/d), NBS domestic production was 18.57 Mt (4.373 mb/d), and NBS processing was
  53.72 Mt (12.650 mb/d). At 7.3 bbl/t, the physical residual is **-15.111 mb**. Varying the
  import conversion alone by +/-2% gives **-19.941 to -10.281 mb**. This is a total-stock /
  balancing residual, not an ownership estimate.
- Why 88 mb appeared:
  - Replacing May customs-total imports with Kpler seaborne arrivals (6.36 mb/d) omits
    **1.430 mb/d / 44.324 mb** of pipeline supply plus tanker-tracking/definition gap and
    changes the implied draw from 15.1 mb to 59.4 mb.
  - Pairing that seaborne number with the separate circulated 13.5 mb/d runs estimate adds
    roughly another 26 mb. Official NBS throughput is 53.72 Mt, or 12.65 mb/d at 7.3 bbl/t;
    13.5 is a different analyst run series/implicit conversion, not that NBS observation.
  - The cited 1.9 mb/d year-on-year runs decline is likewise an analyst series. NBS reports
    May processing down 9.1% y/y; reconstructing its prior-year level implies about a
    1.27 mb/d decline at 7.3 bbl/t. The repo's earlier ~39 mb shortfall uses NBS and remains
    the appropriate like-for-like number.
- Month/sign audit, total-import balance versus seaborne balance in million barrels
  (positive is build):
  - February: about +49.7 versus +17.9; no observed comparator. GAC imports are monthly,
    but NBS publishes January-February production and processing jointly, so those two
    February legs are calendar-day allocations and explicitly flagged.
  - March: +53.9 versus +2.1; both match the IEA +40 mb build sign, total is much closer.
  - April: +13.1 versus -25.0; the seaborne construction has the wrong sign relative to
    Kpler's war-onset-to-mid-May visible-tank build of about 25 mb.
  - May: -15.1 versus -59.4; both can match a late-May draw, but only the official-total
    magnitude is compatible with the roughly -25 mb Kayrros/Energy Aspects May-to-7-June
    observation without demanding a much larger hidden draw.
  - June: -28.1 versus -61.8; both match the IEA -41 mb draw sign, total is closer.
  - July: +6.5 versus -34.2; no observed comparator was located by the cutoff, but the two
    constructions disagree in sign and this is preserved rather than averaged away.
- Conversion sensitivity: central factor is **7.3 bbl/t**. One common +/-2% factor on every
  tonne-denominated May leg barely moves the residual (about -14.8 to -15.4 mb) because it
  mostly cancels. The CSV varies the customs import factor alone, a conservative grade-mix
  test that moves May by +/-4.83 mb. Allowing all three factors to vary independently at
  opposite extremes would span roughly a 30.5 mb draw to a 0.3 mb build, but that mechanical
  worst case assumes adverse, uncorrelated grade errors on every leg.
- Method boundary: the residual absorbs timing, scope, conversion and coverage errors. NBS
  covers industrial enterprises above designated size; tanker vendors differ on Made Island,
  sanctioned/dark cargoes and late destination assignments. No row is attributed to
  government versus commercial stocks. The prior ~20/100 confidence in a large government
  SPR release is unchanged.
- Blog-safe wording: "China's official crude balance points to a modest May stock draw of
  about 15 million barrels, not the widely implied 88 million. The larger figure mixes
  seaborne-only imports with a separate refinery-run estimate; customs-total imports and
  official processing close most of the gap. China did use inventory flexibility, but the
  balance cannot distinguish commercial tanks from government SPR, and public ownership
  evidence still does not support a large government release."
- Source breadcrumbs, accessed 2026-08-20:
  - GAC portal and EIA GAC synthesis: https://english.customs.gov.cn/Statistics/Statistics ;
    https://www.eia.gov/todayinenergy/detail.php?id=67905
  - February and March GAC cross-checks: https://www.interfax.ru/amp/1077014 ;
    https://www.energyconnects.com/news/oil/2026/april/china-s-oil-and-gas-imports-shrink-on-gulf-turmoil/
  - April-May GAC: https://www.marketscreener.com/news/china-energy-imports-drop-in-april-amid-iran-war-as-fuel-exports-hit-decade-low-ce7f5bd8d98af627 ;
    https://www.bairdmaritime.com/amp/story/shipping/tankers/chinas-eight-year-low-in-oil-imports-offers-relief-for-global-prices
  - June-July GAC/Vortexa: https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d ;
    https://www.brecorder.com/news/amp/40433885
  - NBS Jan-Feb through July: https://www.stats.gov.cn/english/PressRelease/202603/t20260317_1962806.html ;
    https://www.stats.gov.cn/english/PressRelease/202604/t20260417_1963350.html ;
    https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html ;
    https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html ;
    https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html ;
    https://www.stats.gov.cn/english/PressRelease/202608/t20260819_1965079.html
  - Kpler seaborne and visible stocks: https://www.hydrocarbonprocessing.com/news/2026/06/chinas-crude-oil-imports-slump-but-its-economics-not-altruism/ ;
    https://archive.is/PJQz3 ;
    https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2
  - Kayrros/Energy Aspects: https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
  - IEA March/June observations: https://www.iea.org/reports/oil-market-report-april-2026 ;
    https://www.iea.org/reports/oil-market-report-july-2026
- Validation: regenerated with `.venv/bin/python`; asserted six ordered monthly rows, exact
  May central/sensitivity outputs, April sign divergence and June draw sign; parsed all 113
  manifest rows at a consistent 15-column width; `git diff --check` passed for scoped files.

- Source leads: China GAC monthly trade statistics (http://english.customs.gov.cn/);
  NBS monthly energy production releases (https://www.stats.gov.cn/english/PressRelease/),
  already cited in `hormuz-what-happened-to-the-barrels.md` refs [16] for Apr/May/Jun 2026;
  JODI oil (https://www.jodidata.org/) as a cross-check on customs.
- The repo's existing NBS-based China crude-processing shortfalls versus year-ago are
  **25 / 39 / 81 mb** for April, May and June. The circulating article's "runs 1.9 mb/d below
  May 2025" implies ~59 mb for May, which does not match the 39 mb figure. Resolve which
  series and which baseline each is using; this is a second, smaller discrepancy worth closing
  in the same pass.
- Note the definitional trap for anyone picking this up: EIA reports China's government-held
  and NOC-commercial stocks together as "strategic oil inventories," so a headline "1.4 bn bbl
  of strategic inventories" is not a government SPR figure.
- Wider methodological point, worth a sentence in whatever this produces: the circulating
  claim is a residual, and residuals absorb every error in every input. This is the same
  failure mode that made the global balance gap look like 308 mb until report vintages were
  matched, and it is why the remaining 130 mb is not read as hidden barrels.
