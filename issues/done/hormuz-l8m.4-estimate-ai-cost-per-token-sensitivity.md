---
id: "hormuz-l8m.4"
title: "Estimate AI cost-per-token sensitivity"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "cost-per-token"
  - "prices"
  - "us-business"
blocked_by:
  - "hormuz-l8m.3"
blocks:
  - "hormuz-l8m.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:03Z"
updated_at: "2026-07-06T17:20:00Z"
---

# Estimate AI cost-per-token sensitivity

## Description

Translate data center electricity cost changes into approximate inference and training cost-per-token impacts using energy-per-token or GPU power assumptions and utilization scenarios.

## Acceptance Criteria

Estimate separates electricity from capex/GPU/labor costs and gives plausible percentage and absolute changes with citations.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-l8m.3` - Estimate US power-price implications for data centers
- Blocks: `hormuz-l8m.5` - Cross-check against macro inflation and energy models

## Work Notes

- 2026-07-06T16:00Z: Claimed for parallel evidence gathering. Depends on `hormuz-l8m.3`; current work should separate electricity sensitivity from GPU/capex/labor costs and prepare formulas that can ingest data-center power price deltas later.
- 2026-07-06T16:20Z: First-pass framework drafted. This is intentionally a sensitivity scaffold, not a precise serving-cost model.

### Core formulas

- Define `p` = electricity price in `$ / kWh`.
- Define `pue` = power usage effectiveness.
- Define `e_it` = IT energy intensity in `Wh / token` (exclude cooling/overhead).
- Then:
  - `kWh_per_1M_tokens = 1000 * e_it`
  - `electricity_cost_per_1M_tokens = kWh_per_1M_tokens * pue * p`
  - equivalently, `electricity_cost_per_1M_tokens = 1000 * e_it * pue * p`
- If starting from hardware power and throughput instead of token energy:
  - `kWh_per_1M_tokens = 277.78 * (W_avg / tok_per_sec)`
  - where `W_avg` is average server power in `kW` and `tok_per_sec` is sustained output throughput.
  - `electricity_cost_per_1M_tokens = 277.78 * (W_avg / tok_per_sec) * pue * p`
- If electricity is only a fraction of total serving cost:
  - let `s_e = electricity_cost / total_serving_cost` at baseline.
  - for an electricity price move of `g = Δp / p`, the total serving-cost impact is `Δtotal / total = s_e * g`.
  - this is the right linear approximation until we have l8m.3 regional power deltas and a better utilization estimate.

### Plausible parameter ranges

- `pue`: 1.09 for Google’s 2024 global fleet; 1.56 as the cited industry average in Google’s page. Practical scenario band here: `1.1-1.6`, with `~1.1-1.2` for very efficient sites and `~1.4-1.6` for generic/older fleets. Source: Google Data Centers, operating sustainably, accessed 2026-07-06: https://datacenters.google/operating-sustainably
- `GPU / node power`: NVIDIA H100 is up to 700W TDP on the H100 page; H100 PCIe is 350W default / up to 700W configurable on product briefs; DGX H100/H200 system power is 10.2 kW max. Source URLs accessed 2026-07-06: https://www.nvidia.com/en-us/data-center/h100/ ; https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html
- `Inference energy intensity`: recent LLM inference studies show very wide spread. Some reported values are per prompt/response rather than directly per token, so normalize carefully before using them in a chart. Practical scenario band for hosted inference: roughly `0.25-4 kWh / 1M tokens` for efficient to moderate deployments, with outliers higher for reasoning-heavy, long-output, or poorly utilized stacks. Source URLs accessed 2026-07-06: https://arxiv.org/html/2505.09598v1 ; https://arxiv.org/html/2407.16893v2
- `Training energy intensity`: training is lumpy and should usually be amortized separately from serving. Publicly cited estimates include GPT-3 at 1,287 MWh for one training run and BLOOM at 433 MWh; recent literature also notes inference can be up to 90% of lifecycle energy. Use training as a separate capex/embodied-energy line, not as a direct per-token serving add-on unless explicitly amortizing over a forecast token volume. Source URLs accessed 2026-07-06: https://news.umich.edu/optimization-could-cut-the-carbon-footprint-of-ai-training-by-up-to-75/ ; https://arxiv.org/html/2505.09598v1
- `Public API price context`: list prices are revenue/user-price context, not serving-cost estimates. OpenAI API prices currently span from sub-$1 to tens of dollars per 1M tokens depending on model and service tier; examples on the official pricing page include GPT-5.4 at $2.50 input / $15 output per 1M tokens and GPT-5.4 mini at $0.75 / $4.50 under standard pricing. Anthropic public pricing shows Haiku 4.5 at $1 / $5, Sonnet 4.6 at $3 / $15, and Opus 4.8 at $5 / $25 per 1M tokens. Source URLs accessed 2026-07-06: https://developers.openai.com/api/docs/pricing ; https://docs.anthropic.com/en/docs/about-claude/pricing

### Provisional assumptions

- Treat electricity as a variable OPEX slice layered on top of a larger serving stack that also includes GPU capex, networking, storage, software, labor, and margin.
- Treat `e_it` as scenario-specific: it changes materially with model size, output length, batching, quantization, and GPU generation.
- Use PUE as an overhead multiplier on IT energy, not as a substitute for utilization.
- For the blog post, present electricity sensitivity as a bounded scenario band, not a point estimate.

### Worked Sensitivity Table

Assumptions for the table below:

- Electricity is the only moving cost line here; GPU capex, networking/storage, software, labor, and margin are held fixed.
- Energy intensity uses the cited hosted-inference band of `0.25-4 kWh / 1M tokens`.
- PUE uses the cited practical range of `1.1-1.6`.
- Power-price shocks use the `hormuz-l8m.3` rule of thumb that a `+$1/MMBtu` gas shock maps to about `+$7/MWh` at the wholesale margin. I bracket that into modest/base/high cases of `+$3`, `+$7`, and `+$14/MWh`.
- Public API prices remain context only, not a cost benchmark.

| Case | Power-price shock | Electricity-only delta per 1M tokens | Electricity bill change at a $50/MWh working base | Implied total serving-cost change if electricity is 5-15% of fully loaded cost |
|---|---:|---:|---:|---:|
| Modest | `+$3/MWh` | `$0.0008-$0.0192` | `+6%` | `+0.3%-0.9%` |
| Base | `+$7/MWh` | `$0.0019-$0.0448` | `+14%` | `+0.7%-2.1%` |
| High | `+$14/MWh` | `$0.0038-$0.0896` | `+28%` | `+1.4%-4.2%` |

- Mid-case check: at `1 kWh / 1M tokens` and `PUE 1.2`, the base case is about `$0.0084` extra per `1M` tokens, which is small in absolute terms because capex/GPU/labor dominate the stack.
- This is a marginal electricity sensitivity, not a claim about provider margins or invoice prices.

### Open blockers

- No public, model-specific disclosure for frontier serving throughput, batching policy, utilization, hardware mix, or amortized capex.
- No public, reliable breakdown of electricity vs capex vs labor in hosted LLM serving cost.
- Regional power deltas from `hormuz-l8m.3` are still pending, so this issue stays as the ingestion layer for those scenarios.
- Need a later pass to separate input-token, output-token, and cached-token economics if we want to compare public API list prices to self-hosted marginal cost.

### Completion Note

- 2026-07-06T17:20Z: Acceptance criteria met. The note now separates electricity from the fixed serving stack, gives both absolute and percentage sensitivities, and keeps API pricing explicitly labeled as context rather than cost.
