---
id: "hormuz-p2k.11"
title: "Model what happens if demand reduction has to scale up"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "demand"
  - "scenarios"
  - "durability"
blocked_by:
  - "hormuz-p2k.10"
children: []
blocks: []
owner: "p2k_demand_scaling"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T23:00:00Z"
---

# Model what happens if demand reduction has to scale up

## Description

This is the payoff question of the durability epic and it is currently unanswered. The
marginal-absorber timeline in `docs/hormuz-shock-absorption-durability.md` says the marginal
barrel shifts toward demand adjustment, but never says **by how much** or **what that would
mean where it lands**.

The intended chain of reasoning:

1. Stocks, bypass and non-Gulf supply provide a quantifiable mb/d of headroom, bounded by
   `p2k.8` for stocks and `p2k.7` for bypass.
2. That headroom runs to a date, after which the residual shortfall must be absorbed by
   demand reduction.
3. Demand reduction to date has run at roughly **3.6 mb/d** (439.2 mb over 122 days), about
   3.5% of global consumption, concentrated in specific countries and sectors.
4. If that has to rise by some factor, **where does the increment physically land, and what
   does it do there?**

Step 4 is the deliverable. It should be answered with country and sector evidence, not with
an elasticity parameter, since `p2k.6` already concluded that no transferable elasticity or
conservation half-life can be recovered from historical shocks.

## Acceptance Criteria

- A stated mb/d headroom figure from the non-demand channels, with the date at which it is
  exhausted under continued current Strait traffic, drawing on `p2k.7`, `p2k.8` and `p2k.9`.
- Demand-reduction scaling scenarios at roughly 1.25x, 1.5x and 2x the current 3.6 mb/d, each
  expressed as an increment in mb/d.
- For each scenario, a country-and-sector landing analysis: which economies and which
  end-uses would have to supply the increment, given that the cheap tier-1 substitution is
  capped by installed capacity and the tier-2 industrial cuts are already deep in China,
  Japan and South Korea.
- An explicit qualitative statement of consequences per scenario, in the form the project
  actually wants: "demand reduction has primarily happened in X, Y and Z; if it had to rise
  by factor F, the increment would most likely land in A and B, exacerbating conditions in
  the following specific ways."
- Tier-3 transition candidates named, with the evidence for why those specific places are
  the fragile ones.
- No implied precision: scenarios are illustrative bounds on where pressure lands, not
  forecasts of what will happen.

## Notes

Depends on `p2k.10`, because the scaling analysis is meaningless while 56% of the demand gap
sits in two undifferentiated regional buckets. The countries most likely to absorb an
increment are disproportionately inside those unresolved buckets.

The existing tier examples are the right raw material: tier-2 refinery and petrochemical cuts
in China, Japan and South Korea; tier-3 cooking-LPG exposure in India and Kenya; rationing in
Myanmar; schooling and work-schedule changes in Lao PDR; fishing-livelihood losses in the
Philippines; freight and food-system risk in fragile African importers.

## Source Leads

- `data/derived/hormuz_p2k_3_demand_cost_tier_matrix.csv`
- `data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv`
- IEA 2026 energy crisis policy response tracker
- Country reporting on rationing, fuel queues, aviation capacity and industrial curtailment

## Work Notes

- 2026-08-06: Claimed for implementation. The scenario model will distinguish already-running absorber flows from unused headroom, retain stock dates as bounded fixed-rate mechanics rather than operating forecasts, and use `p2k.10` country allocations plus `p2k.3` sector/cost evidence for the landing analysis.
- 2026-08-06: Built `scripts/build_p2k_11_demand_scaling_scenarios.py` and generated 45 rows in `data/derived/hormuz_p2k_11_demand_scaling_scenarios.csv`. Registered the artifact in `data/manifest.csv`.
- Historical denominator: the matched March-June `p2k.10` world vintage gap is 439.228 mb over 122 days, or 3.600 mb/d. The 1.25x, 1.5x and 2x scenarios are 4.500, 5.400 and 7.200 mb/d, increments of 0.900, 1.800 and 3.600 mb/d.
- Current-versus-incremental discipline: roughly 3.4 mb/d of bypass flow and the 2.197 mb/d average implied by 290 mb over 132 days of collective stock execution are **already-running/historical absorber flows**, not new headroom. The only identified new flow is 0/0.053/0.702 mb/d low/base/high: the positive part of the `p2k.9` no-reopening balance plus, only in the high case, Iraq's undemonstrated 0.2 mb/d Ceyhan sensitivity. Additional global stock draw-rate capacity remains unknown and gets no credit.
- After that new-flow envelope, residual scenario increments are 0.900/0.847/0.198 mb/d at 1.25x, 1.800/1.747/1.098 mb/d at 1.5x, and 3.600/3.547/2.898 mb/d at 2x (low/base/high headroom respectively).
- Stock dates are deliberately bounds, not a false exhaustion forecast. At 2.197 mb/d, the IEA's **greater-than** 1 bn barrel gross level implies physical zero **no earlier than** 2027-10-19, while legal/operational/product floors can bind before that. At the July 0.596 mb/d U.S. draw, gross physical zero on 2027-12-24 is the latest fixed-rate endpoint; the usable operating interval is 0-512 days because the floor is unpublished. April aggregate 0-46 days of statutory public-stock headroom cannot be converted into release duration without country ownership and rate data. Therefore no honest single usable-stock exhaustion date is identified.
- A separate mechanical sensitivity shows why this matters: if a future collective stock flow equal to the 2.197 mb/d historical average were present and then stopped, required demand adjustment would rise to 6.697, 7.597 and 9.397 mb/d in the three scenarios. This is explicitly not evidence that such a flow is continuing or committed.
- Country/sector landing rows close each increment using a pro-rata continuity benchmark over the positive `p2k.10` gap (454.917 mb; North America's negative revision is excluded). Northeast Asian refining/petrochemicals are 28.9% of that benchmark; the fragile and diversified Gulf clusters together 29.6%; Southeast Asia 12.3%; India 7.4%; other Asia/Oceania 7.7%; other positive regions 8.2%; and Africa 5.8%. These are low-fidelity pressure anchors, not country forecasts. Qualitative pressure ordering instead uses `p2k.3`: installed tier-1 switching persists but is capped; large marginal volumes first deepen Northeast Asian and Gulf tier-2 industrial/service losses, while smaller tier-3 harm appears in Indian/Kenyan LPG, Myanmar rationing, Lao schooling/work schedules, Philippine fishing, and fragile Gulf activity.
- Interpretation: 1.25x is still a tier-2-sized increment but extends refinery/petrochemical, aviation and mobility losses and widens existing tier-3 pockets. At 1.5x, efficiency alone is not credible; industrial and service cuts deepen and cooking/freight/food stress spreads. At 2x, the increment equals the entire historical demand adjustment again and plausibly requires broad transport/industrial contraction plus materially more essential-service failure.
- Validation: compiled and reran the builder in the repository `.venv`; checked 45 unique row IDs, fixed-width CSV output, exact positive-cluster closure and exact scenario-allocation closure. No price assumption or elasticity is used.
