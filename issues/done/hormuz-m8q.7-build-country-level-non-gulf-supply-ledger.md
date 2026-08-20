---
id: "hormuz-m8q.7"
title: "Build country-level non-Gulf oil-supply ledger"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "supply"
  - "country-ledger"
  - "2026-actuals"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "codex"
created_at: "2026-08-04T00:00:00Z"
updated_at: "2026-08-04T01:00:00Z"
---

# Build country-level non-Gulf oil-supply ledger

## Description

Quantify March-July 2026 oil-production revisions by material supplier against the frozen February 2026 EIA STEO, while keeping actual production separate from cargo redirection, stock releases, and announced-but-not-observed production commitments.

## Acceptance Criteria

- Monthly and cumulative March-July country rows use the same EIA liquids taxonomy and February/July vintages.
- Preliminary March-June estimates and the July forecast are explicitly labelled.
- Material positive and negative revisions are shown; small countries remain available in the machine-readable ledger.
- IEA statements on Atlantic Basin exports and the Americas supply response are retained as cross-checks, not added to production.
- Canada and Mexico's collective-action production commitments are reconciled with the EIA realized/forecast-vintage panel.
- The country ledger preserves unallocated and classification residuals instead of forcing a false match to the global shortfall.

## Work Notes

- 2026-08-04: Claimed. The primary calculation will compare EIA STEO Table 3b petroleum and other liquid fuels production in the frozen 10 February workbook with the 7 July publication (model completed 1 July). This is a consistent counterfactual revision, not proof that each production change was caused by Hormuz.
- 2026-08-04: Built `data/derived/hormuz_m8q_7_nongulf_supply_ledger.csv` with a reproducible standard-library XLSX extractor in `scripts/build_m8q_7_nongulf_supply_ledger.py`. It contains monthly and March-July summaries for 19 common country rows, complete regional checks, an exact EIA Table 3c global identity, and non-additive IEA trade/policy context rows.
- 2026-08-04: Main production result: the Americas supplied **119.98 million barrels more** than the frozen February forecast over March-July. North America contributed +79.92 mb and Central/South America +40.06 mb. The material named gains are the United States **+77.98 mb** and Brazil **+35.48 mb**, followed by China +7.83 mb, Kazakhstan +3.71 mb, Guyana +3.60 mb, Mexico +3.48 mb, Argentina +3.13 mb, Oman +2.91 mb, and Azerbaijan +1.53 mb. Numbers smaller than roughly 5 mb are useful audit rows but generally rounding-detail for the final narrative.
- 2026-08-04: The Americas gain did not translate one-for-one into a world cushion. Europe, Eurasia, Africa, and Asia/Oceania together revised down by **60.99 mb**, led by Russia -39.11 mb, Malaysia -9.31 mb, India -9.13 mb, Norway -6.80 mb, and smaller changes. The complete non-Middle-East regional net is therefore **+59.00 mb**. Oman adds +2.91 mb if treated as a non-Hormuz-route regional supplier. This is much smaller than the gross Americas response and is the better net supply-side accounting number.
- 2026-08-04: The common named-country ledger shows +139.66 mb of positive revisions and -68.01 mb of negative revisions, net +71.65 mb. The difference from the complete regional net is the combined contribution of countries that Table 3b leaves inside regional aggregates. Preserve it as group residual rather than inventing country allocations.
- 2026-08-04: IEA cross-checks support the direction and geography. The May OMR said 2026 Americas supply growth had been revised up by more than 0.6 mb/d since the start of the year, to 1.5 mb/d. The EIA Americas March-July revision averages about 0.784 mb/d, a compatible but not identical measure. IEA also named the United States, Kazakhstan, Brazil and Venezuela as the largest output gains supporting Atlantic-to-Asia flows.
- 2026-08-04: The IEA's **3.5 mb/d** increase in Atlantic Basin crude exports East of Suez is deliberately not converted to cumulative new supply. The June OMR says it reflects robust Americas growth **and steep US SPR releases**; IEA's 22 June commentary adds that US crude exports were supported by higher production and industry/government stock draws. It therefore mixes production, inventory release and redirection of existing cargoes.
- 2026-08-04: Canada is an important failed reconciliation. The IEA's 19 March provisional collective-action table labelled **23.6 mb** from Canada as a production increase, yet the July-vintage EIA panel is **1.54 mb below** the frozen February forecast cumulatively through July. Treat the 23.6 mb as an announced policy contribution, not observed incremental supply, until a Canadian primary production series proves delivery. Mexico's 3.9 mb commitment is close to the EIA +3.48 mb revision and should be treated as overlapping rather than added.
- 2026-08-04: The exact EIA Table 3c forecast-revision identity closes: world -1,724.36 mb = OPEC+ -2,051.41 mb + United States +77.98 mb + non-OPEC+ excluding US +249.06 mb. This is retained only as a scale check. OPEC/OPEC+ membership and regional classification changed across the two workbooks, so the +249.06 mb group must not be labelled a clean non-Gulf cushion.
- 2026-08-04: No arbitrary low/base/high causal-attribution band was manufactured. The EIA vintage differences are exactly reproducible, but the fraction caused by Hormuz is not identified country by country. The defensible final language is “production above/below the frozen pre-war forecast, which cushioned/worsened the shock,” supplemented by IEA qualitative attribution.
- 2026-08-04: Validation passed: 19 countries x 5 months plus 19 country summaries; country cumulative rows equal their month sums; complete regional aggregates are non-overlapping; Table 3c global identity closes within 0.01 mb; script regenerates; Python compilation and `git diff --check` pass.

## Source Breadcrumbs

- EIA STEO February 2026 workbook: https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
- EIA STEO July 2026 workbook: https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx
- IEA May 2026 OMR: https://www.iea.org/reports/oil-market-report-may-2026
- IEA June 2026 OMR: https://www.iea.org/reports/oil-market-report-june-2026
- IEA 22 June supply-adjustment commentary: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
- IEA 19 March collective-action contribution table: https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
