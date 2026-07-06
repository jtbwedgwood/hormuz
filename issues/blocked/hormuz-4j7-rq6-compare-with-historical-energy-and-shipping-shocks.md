---
id: "hormuz-4j7"
title: "RQ6: Compare with historical energy and shipping shocks"
type: "epic"
status: "blocked"
priority: "P2"
parent: null
labels:
  - "comparisons"
  - "history"
blocked_by:
  - "hormuz-s49"
blocks:
  - "hormuz-ccx"
children:
  - "hormuz-4j7.1"
  - "hormuz-4j7.2"
  - "hormuz-4j7.3"
  - "hormuz-4j7.4"
  - "hormuz-4j7.5"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:10Z"
updated_at: "2026-07-06T06:09:10Z"
---

# RQ6: Compare with historical energy and shipping shocks

## Description

Build a rigorous comparison between the current Hormuz disruption and prior shocks such as 1970s oil crises, 2002 Venezuela strike, 1990 Gulf crisis, 2011 Libya, 2019 Abqaiq, and COVID logistics disruptions.

## Acceptance Criteria

Comparable metrics are normalized; selected analogues are justified; the comparison avoids naive barrel-only claims and highlights structural differences.

## Dependency Notes

- Cleared dependency: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Cleared dependency: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Child: `hormuz-4j7.1` - Select historical shock comparison cases
- Child: `hormuz-4j7.2` - Define normalized comparison metrics
- Child: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Child: `hormuz-4j7.4` - Rank current Hormuz shock against historical analogues
- Child: `hormuz-4j7.5` - Produce historical comparison graphic

## Work Notes

- 2026-07-06T06:32Z: Claimed parent epic for parallel work. Spawned subagents with non-overlapping issue ownership:
  - `hormuz-4j7.1` historical case selection: research comparison cases, cite sources, and mark done if acceptance criteria are met.
  - `hormuz-4j7.2` normalized comparison metrics: draft a provisional metric framework while waiting on final case selection.
  - `hormuz-4j7.3` data reconnaissance: document blockers, source families, candidate series, data gaps, and future schema without claiming the dataset is complete.
- Current dependency status: `hormuz-4j7.1` is unblocked because `hormuz-fyp.1` is done. `hormuz-4j7.2` is logically blocked on `hormuz-4j7.1` but can advance provisionally. `hormuz-4j7.3` remains blocked by in-progress RQ1/RQ2/RQ4/RQ5 work plus `hormuz-4j7.2`. `hormuz-4j7.4` and `hormuz-4j7.5` are not ready except for handoff/blocker notes.
- 2026-07-06T08:08Z: Completed all currently unblocked work and moved epic to `issues/blocked/`.
  - Done: `hormuz-4j7.1` selected historical comparison cases with dates, affected supply, duration, market context, rationale, confidence, exclusions, and source breadcrumbs.
  - Done: `hormuz-4j7.2` defined normalized metrics and table fields for rigorous historical comparison.
  - Blocked: `hormuz-4j7.3` has source/data reconnaissance and a future schema but cannot produce the cited dataset until RQ1/RQ2/RQ4/RQ5 inputs arrive.
  - Blocked: `hormuz-4j7.4` and `hormuz-4j7.5` should wait for the dataset/ranking; no placeholder ranking or graphic was produced.
- 2026-07-06: Continuation pass after more upstream files appeared. RQ2 has materially advanced: `hormuz-kmz.6` and `hormuz-kmz.7` are done, and derived tables now exist for current disruption scenarios, product disruption ranking, and PortWatch-based daily Hormuz calls. Spawned subagents to update:
  - `hormuz-4j7.3`: map newly available current-Hormuz denominators and partial data into the historical metric collection plan.
  - `hormuz-4j7.4`: define a transparent ranking rubric and hypotheses without producing final rankings from incomplete data.
  - `hormuz-4j7.5`: specify the final historical comparison graphic without fake placeholder values.
  Subsequent local refresh found `hormuz-2y7.6`, `hormuz-kmz.3`, and `hormuz-l8m.1` are now done, so `hormuz-4j7.3` was updated to use the public 2019+ PortWatch backfill boundary, current low/base/high disruption tables, and current low/base/high price-scenario inputs. Remaining hard blocker is `hormuz-s49.6` for stockpile buffer duration.
- 2026-07-06 cleanup clarification: RQ6 is now blocked only by `hormuz-s49`, specifically the consolidated buffer-duration work in `hormuz-s49.6`. Historical metric collection itself is tracked as child task `hormuz-4j7.3`.
