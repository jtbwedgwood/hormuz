---
id: "hormuz-r3v.7"
title: "Decompose the IEA balance into supply and demand to locate the interagency gap"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "residual"
  - "interagency"
  - "balance"
blocked_by: []
blocks: []
children: []
owner: "codex-root"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T23:59:00Z"
---

# Decompose the IEA balance into supply and demand to locate the interagency gap

## Description

`hormuz-r3v.6` established that the residual is model- and vintage-dependent. This task
locates *where* the interagency disagreement actually sits, which is currently unknown and
has been mis-attributed once already.

### Audit result

The issue's starting comparison was itself misspecified. The **261.36 mb** item was built by
subtracting successive-vintage monthly OPEC+ crude production from a quarterly call-on-DoC
number. That is not the IEA identity of global demand minus total oil supply. It is therefore
retired as a total-oil balance, along with the claimed fixed 2.83 mb/d EIA-IEA gap and the
"same-agency near-closure" inferred from it.

The finest defensible public match is Q2:

| Q2 2026, mb/d | EIA | IEA | EIA minus IEA contribution |
|---|---:|---:|---:|
| Demand | 100.354 | 99.100 | **+1.254** |
| Supply | 95.260 | 96.115 | **+0.856** |
| Implied draw | 5.094 | 2.985 | **+2.110** |

Thus lower IEA demand explains **59.4%** of the matched Q2 draw difference and higher IEA
supply explains **40.6%**. The components close exactly.

The bypass hypothesis fails its available public test. The July IEF table places **0.8 mb/d**
of the 0.856 mb/d supply difference in *non-DoC supply plus DoC NGLs* (64.9 IEA versus 64.1
EIA). Only **0.056 mb/d** remains after that rounded bucket, too small and imprecise to
establish extra IEA credit for Gulf crude rerouting. This does not prove both agencies assign
identical route flows; it shows that the aggregate public discrepancy is located elsewhere.

An exact March-June split cannot be recovered publicly because the revised monthly IEA March
demand level is not exposed. Keeping March supply at the published 97.0 mb/d and using
transparent demand anchors gives an illustrative IEA March-June draw of **299.5 / 426.0 /
494.8 mb**, versus EIA's 606.171 mb, and therefore an EIA-minus-IEA gap of **306.7 / 180.1 /
111.4 mb**. The anchors are scenarios, not a confidence interval. Reproducing the old 261.36
mb point would require March demand of **96.67 mb/d**, below the published 97.9 mb/d May
  nadir, which is an additional warning rather than the reason for rejection; the decisive
  problem is the mismatched accounting scope.

The OPEC premise also reverses under matched categories. OPEC Q2 demand is 3.346 mb/d above
EIA, but its comparable non-DoC supply plus DoC NGL level is **1.2 mb/d lower**, not roughly
3 mb/d higher. The approximately 304 mb demand-level coincidence is not a mechanism and the
project must not describe OPEC's demand and supply ledgers as parallel upward offsets.

## Acceptance Criteria

- IEA monthly world supply and demand for March-June 2026 at the finest granularity public
  sources allow, with an explicit statement of what remains subscriber-only.
- The 2.83 mb/d EIA-versus-IEA balance gap split between its demand-side and supply-side
  components, or an explicit finding that the split cannot be made publicly.
- A test of whether IEA credits more Gulf bypass and replacement supply than EIA, using the
  country and route detail already in `hormuz_m8q_6_gulf_physical_oil_ledger.csv` and
  `hormuz_m8q_7_nongulf_supply_ledger.csv`.
- The EIA-versus-OPEC scope difference characterized: confirm whether the roughly parallel
  ~3 mb/d offset on both supply and demand reflects known definitional differences such as
  biofuels, NGL and processing-gain treatment.
- The coincidental 304 mb demand-difference match explicitly retired in any document that
  currently implies it is causal.
- If the IEA-versus-EIA gap turns out to be supply-side, propagate to `hormuz-p2k.7` and the
  bypass sensitivity range.

## Notes

The r3v.7 audit supersedes one caveat from `r3v.6`: the 261.36 mb figure is not merely a
non-subscriber reconstruction but an invalid total-oil comparator. OPEC's 672.3 mb is built from quarterly
proxies with March inheriting the 1Q average, so part of the EIA-OPEC distance is this
project's own construction; and agency balances share country submissions, so they are not
independent estimates.

Also record the structural point that makes this residual unavoidable: **EIA publishes no
global observed-stock series.** Any comparison of a global balance against observed global
inventories must cross institutions, because the IEA is effectively the sole source for the
observed side.

## Source Leads

- IEA Oil Market Report public tables and highlights, March-July 2026
- `data/derived/hormuz_r3v_4_third_source_balance.csv`
- `data/derived/hormuz_m8q_1_monthly_oil_balance.csv`
- OPEC MOMR world oil demand and supply tables for scope definitions
- IEF agency-comparison work on definitional differences: https://www.ief.org/

## Work Notes

- 2026-08-06: Claimed by the parent agent. The audit will separate three questions that the
  current issue partially conflates: the EIA-versus-IEA **net balance** difference, the
  independently observable supply-level difference, and taxonomy/scope offsets that can move
  both supply and demand without changing the balance. Public headline levels will be kept
  distinct from the subscription-only revised IEA monthly table.

- 2026-08-06 p2k.12 handoff: use **298 mb total observed draw** and **308.171 mb** as the
  same-bound headline residual. The onshore-accessible diagnostic is 316/351/386 mb, but its
  apparent 18/53/88 mb narrowing is a boundary mismatch unless the implied balance is also
  restated to exclude oil on water. March global oil on water fell 117 mb; the separate
  +100 mb Gulf floating build is nested within that decline. Do not describe the 100 mb as
  a global build or use the retired 568 mb arithmetic.

- 2026-08-06: Completed the public-input audit and reproducible decomposition in
  `data/derived/hormuz_r3v_7_interagency_balance_decomposition.csv` (37 rows), generated by
  `scripts/build_r3v_7_interagency_balance_decomposition.py`. Public IEA monthly total supply
  is 97.0/95.1/94.5/98.8 mb/d for March-June; matched July-vintage public IEA demand is
  quarterly (104.2 in Q1, 99.1 in Q2), with only the May monthly nadir of 97.9 public.

- 2026-08-06: The exact public Q2 EIA-minus-IEA implied-draw gap is **2.109630 mb/d**.
  Demand contributes **1.253928 mb/d (59.438%)** and supply contributes **0.855702 mb/d
  (40.562%)**. The rounded IEF outside-DoC/NGL supply bucket accounts for 0.8 mb/d, or 93.5%
  of that supply component; the 0.055702 mb/d remainder is below useful attribution scale.

- 2026-08-06: Retired the 261.36 mb IEA reconstruction and its same-agency near-closure.
  The public Q2 balance alone implies 271.6 mb drawn; forcing the four-month total down to
  261.36 mb requires March demand of 96.67 mb/d, below the published May nadir. The artifact
  instead publishes a transparent March-demand sensitivity: IEA draw 299.5/426.0/494.8 mb
  and EIA-minus-IEA gap 306.7/180.1/111.4 mb. These anchors do not alter the separate
  same-bound EIA-minus-observed-stock diagnostic of 308.171 mb.

- 2026-08-06: Corrected the OPEC interpretation. Its Q2 demand is 3.346 mb/d above EIA, but
  the matched outside-DoC/NGL supply category is 1.2 mb/d lower. The apparent 304 mb match
  is coincidental and the claimed parallel +3 mb/d supply/demand offset is false. IEF's
  method note also records scope differences: EIA country supply includes biofuels and
  processing gains, OPEC includes biofuels, and IEA excludes both, while IEF normalizes its
  aggregate non-OPEC table.

- 2026-08-06: Propagated the correction into the synthesis document, deprecated the legacy
  r3v.4 IEA and residual-range rows in both its builder and output, and registered the new
  artifact in `data/manifest.csv`. Replaced r3v.1's invalid cross-agency range with a
  same-EIA-balance, observed-stock-vintage plug sensitivity of 238.171/308.171/347.571 mb;
  total T4 is now 352.284/422.284/461.684 mb. No p2k.7 bypass range changes: the aggregate
  evidence does not support extra IEA Gulf-bypass credit.
