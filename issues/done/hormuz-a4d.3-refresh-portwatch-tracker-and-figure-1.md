---
id: "hormuz-a4d.3"
title: "Refresh the PortWatch daily tracker and Figure 1 through publication date"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-a4d"
labels:
  - "tracker"
  - "portwatch"
  - "figure"
  - "blog"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T00:00:00Z"
---

# Refresh the PortWatch daily tracker and Figure 1 through publication date

## Description

Figure 1 is the draft's opening visual and its caption claim is that traffic "has never come
close to prewar levels." The local pull ends **2026-07-23**, which is roughly four weeks stale
for a mid-August post and leaves the entire post-re-closure period undocumented.

1. Re-run `scripts/fetch_portwatch_hormuz.py` and `scripts/build_public_hormuz_tracker.py`
   to the latest public observation.
2. Replace the 2026-07-24 to 2026-07-31 **nowcast** in `docs/hormuz-ship-tracker.md` with
   observed data, and check whether the nowcast (85 total / 28 tanker calls) was right.
3. Recompute regime means: the 2026-07-08 onward low regime (July vintage: 10.6 total/day =
   11.7% of baseline, 3.5 tanker/day = 6.4% of baseline) and any distinct August regime.
4. Confirm or correct the draft's "never come close to prewar levels" sentence against the
   full series, including the June peak (2026-06-24 to 07-07 averaged 31.9 total / 15.5
   tanker, versus a 90.5 / 54.8 baseline).
5. Refresh `figures/fig-2y7-public-hormuz-daily-transits.svg` and its data CSV, and update
   `data/derived/hormuz_m8q_2_current_traffic_scenario.csv` if the held-constant scenario
   rate no longer matches observation.
6. Re-check the ArcGIS layer's last-edited date and re-flag the provisional tail.

## Acceptance Criteria

- Tracker CSV, figure, and figure data extend to within a few days of the publication date.
- No nowcast values remain inside the observed-history portion of the chart.
- Updated regime means with the July-vintage values shown alongside for comparison.
- `docs/hormuz-ship-tracker.md` "Last updated" and cutoff lines refreshed.

## Dependency Notes

- Parent: `hormuz-a4d`

## Work Notes

- 2026-08-18: Claimed for the publication-date refresh. The tracker, fetch/build scripts,
  manifest, documentation, widget and figures already contain uncommitted July-refresh work;
  this task will preserve and extend those changes rather than recreate or revert them.
- 2026-08-18: Refetched the authoritative IMF PortWatch `Daily_Chokepoints_Data` ArcGIS
  layer, filtered to `portid='chokepoint6'`. The pull contains 2,785 continuous, unique daily
  observations from 2019-01-01 through 2026-08-16. Layer metadata reported
  `lastEditDate=2026-08-18T12:34:23.600Z`; the two-day tail remains provisional because the
  public layer exposes no per-row final/revision flag. Source endpoint:
  https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0
- 2026-08-18: The refresh is a source-vintage break, not merely a tail append. Versus the
  prior local July pull, 2,721 of 2,761 overlapping total-call rows and 2,669 tanker rows
  changed. The 2019-2024 baselines are now 75.281 total and 45.680 tanker calls/day, versus
  90.515 and 54.827 in the July vintage. Documentation warns readers not to interpret this
  historical revision as new traffic.
- 2026-08-18: Recomputed windows. June 24-July 7 is 24.571 total / 12.929 tanker calls/day
  (32.6% / 28.3% of revised baselines), versus July-vintage 31.86 / 15.50. July 8-August 16
  is 4.125 / 1.425 (5.5% / 3.1%), versus the July-vintage July 8-23 estimate 10.625 / 3.5
  (11.7% / 6.4%). August 1-16 is 3.812 / 1.250, close to revised July 8-31 at 4.333 / 1.542,
  so there is not yet evidence for a distinct August regime.
- 2026-08-18: Checked the July 24-31 nowcast against observed history. Actual calls were
  29 total / 7 tanker versus the old 85 / 28 forecast: overestimates of 56 (65.9%) and 21
  (75.0%). The scenario builder now omits every horizon at or before `data_as_of`, leaving
  six future-only September/December/March rows based on the revised July 8-August 16 mean.
- 2026-08-18: Claim verdict: retain only with a sustained-traffic qualifier. After June 17,
  the maximum seven-day averages were 26.71 total on June 30 and 13.29 tanker on July 7,
  about 35.5% and 29.1% of baseline. Daily peaks were materially higher (44 total and 21
  tanker), so the docs explicitly distinguish sustained averages from single days.
- 2026-08-18: Regenerated tracker CSV, figure CSV/SVG, scenario CSV, and interactive widget;
  updated cutoff/source metadata and fixed widget baseline/fetch-date/static metrics. Validation
  passed: scripts compile; all 2,785 dates are continuous and unique; class sums reconcile;
  tracker and figure CSVs match; scenario horizons are strictly future and arithmetic matches;
  SVG/widget show the 2026-08-16 cutoff and revised 75.3 total/day baseline; no July-nowcast
  row remains.
