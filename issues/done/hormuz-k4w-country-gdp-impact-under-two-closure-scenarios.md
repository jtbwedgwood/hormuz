---
id: "hormuz-k4w"
title: "Country GDP impact under two closure scenarios"
type: "epic"
status: "done"
priority: "P1"
parent: null
labels:
  - "gdp"
  - "macro"
  - "scenarios"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children:
  - "hormuz-k4w.1"
  - "hormuz-k4w.2"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T20:45:00Z"
---

# Country GDP impact under two closure scenarios

## Description

The blog post needs 2026 GDP impact estimates for both sides of the shock, under two
explicit closure scenarios. The repo currently has **no GDP forecasts of any kind**. The only
existing macro material is a rough gross-export-value-over-nominal-GDP exposure table in
`docs/hormuz-energy-shock-followups.md`, which that document itself flags as "useful for
scale, not national-accounts accounting," plus consumer-side oil-price elasticities collected
in `hormuz-l8m.5`.

**Two deliberately different methods**, because the evidence differs on each side:

- **Gulf producers:** derive a **floor** ourselves from observed production shut-ins. We have
  monthly country-level shut-in data through July, so the direct hydrocarbon channel is
  computable. Publish it as a floor and name the excluded channels rather than modelling them.
- **Consumers (China, India, Southeast Asia, Japan, Korea):** take **official forecasts** and
  audit their assumptions, then re-time them. We cannot credibly build our own macro models
  for oil importers, but we can say what each forecaster assumed and what changes if that
  assumption is wrong.

**Two scenarios**, defined once in `k4w.1` and reused unchanged in `k4w.2`:

- **Scenario A — full reopening 30 September 2026**, with an explicit and sensitivity-tested
  recovery ramp. Production does not snap back on the reopening date: the repo's supplier
  analysis notes shut-in oil stays in the reservoir and missed daily supply is not instantly
  recovered, and EIA's own August baseline reaches near-normal patterns only in early 2027
  even under gradual resumption from September.
- **Scenario B — no reopening during 2026**, current managed-partial-closure regime persists.

## Why the two methods have the same bias

Worth stating in whatever this produces, because it affects how the results should be read:
**both approaches understate the damage, for different reasons.** The producer floor excludes
every non-hydrocarbon channel. The consumer forecasts transmit oil shocks through *price*,
which misses the physical rationing that the repo's own demand work says dominated in Asia —
India's LPG scarcity, refinery and feedstock curtailment, grounded aviation. Neither number is
a central estimate, and the post should not present them as if they were.

## Scope note

This necessarily pulls in **LNG** (Qatar is an LNG economy, not an oil economy) and the wider
macro apparatus, both outside the post's stated oil-only scope. Flag it in the post rather
than quietly widening the frame.

## Acceptance Criteria

- Producer-side floors and consumer-side audited forecasts for both scenarios, in one table
  the blog can use directly.
- Every figure labelled **real or nominal** and **level decline or growth revision**. This is
  the single most common way these numbers get misread; a "−6%" in the wild is usually a
  growth revision.
- Scenario definitions identical across both child tasks.
- Explicit statement of which channels each method omits.

## Dependency Notes

- Blocks: `hormuz-ccx.5` - Draft blog post from evidence package

## Work Notes

- 2026-08-20: Both children completed. Shared scenario mechanics live in
  `data/derived/hormuz_k4w_scenarios.csv`; producer and consumer builds consume the same
  monthly factors. The blog-ready synthesis is `docs/hormuz-country-gdp-impact-scenarios.md`.
- 2026-08-20: The producer table is explicitly real GDP level decline versus a no-shut-in
  counterfactual. The consumer table is real GDP growth and forecast revision. The document
  keeps those units separate and explains why both methods understate non-price/omitted damage,
  while Qatar/UAE mixed oil-gas shares introduce an additional non-floor caveat.

## Completion Note

Acceptance criteria are met: two identical scenarios, producer floors/proxies, audited and
re-timed consumer forecasts, one blog-facing table set, clear real/nominal and level/revision
labels, and explicit omitted-channel and physical-rationing caveats.
