---
id: "hormuz-p2k.9"
title: "Decompose the forward surplus and its embedded reopening assumption"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "surplus"
  - "forecast-conditionality"
  - "durability"
blocked_by: []
blocks: []
children: []
owner: "p2k_surplus_decomposition"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T18:45:00Z"
---

# Decompose the forward surplus and its embedded reopening assumption

## Description

`hormuz-p2k.5` concluded that the 396.1 mb foregone build is "fully spent," which is correct
for that specific channel. But the durability document then omits the forward path entirely,
leaving a natural and important question unanswered: **was the world expecting a permanent
glut, and is any surplus expected to return?**

The data already exists in `data/derived/hormuz_p2k_5_foregone_build_capacity.csv` and
answers the question clearly. Implied global balance, mb/d:

| Period | Frozen February | Post-shock July |
|---|---:|---:|
| 2026-09 | +2.53 | -1.37 |
| 2026-10 | +4.00 | **+2.36** |
| 2026-12 | +2.11 | +2.57 |
| 2027-06 | +1.61 | +3.50 |
| 2027-12 | +1.53 | +4.78 |

So EIA's own post-shock vintage expects the deficit to end around **October 2026** and 2027
to run a **larger** surplus than February had projected. The market was never expected to be
in permanent glut, and it is not expected to be in permanent deficit either.

### The problem, and why this needs work rather than simple restatement

That forward surplus almost certainly **embeds an assumption of Hormuz normalization**. EIA
would not project a +4 to +6 mb/d surplus through 2027 while assuming the Strait remains at
current partial flow. So the surplus is not independent headroom that could absorb further
disruption; to a large and currently unquantified degree it is a restatement of "if the
Strait reopens, the balance recovers."

Excluding it from the durability timeline was therefore defensible. **Omitting the number
without explanation was not.** A reader cannot evaluate a forward analysis that silently
drops the forecast's own forward path.

## Acceptance Criteria

- The July-vintage forward balance path published in the durability document, with the
  deficit-to-surplus crossover date stated.
- The Gulf supply-recovery assumption embedded in the July STEO identified as explicitly as
  public documentation allows: what Gulf production and Hormuz flow path does the July
  vintage assume for late 2026 and 2027?
- A decomposition, or a bounded estimate, of how much of the projected 2027 surplus survives
  a no-reopening assumption. This is the number the durability epic actually needs.
- An explicit statement of why the surplus is or is not creditable as absorption headroom,
  replacing the current silent omission.
- If the embedded assumption cannot be recovered from public STEO documentation, say so
  directly and treat the entire forward surplus as non-creditable, with reasoning.

## Notes

Watch for circularity. If the July vintage assumes reopening, then using its forward surplus
to argue the shock is survivable is assuming the conclusion. The honest framing is likely
two-branch: under reopening the balance recovers on EIA's own numbers; under continued
closure the forward surplus is largely unavailable and the marginal absorber stays demand.

## Source Leads

- `data/derived/hormuz_p2k_5_foregone_build_capacity.csv`
- EIA STEO July 2026 report text and assumptions: https://www.eia.gov/outlooks/steo/archives/jul26.pdf
- EIA STEO February 2026 workbook for the pre-war counterfactual path

## Work Notes

- 2026-08-06: Claimed by `p2k_surplus_decomposition`. The audit will keep three
  concepts separate: EIA's published reopening branch, a mechanical continuation
  of the July partial-flow supply loss, and the non-Gulf/non-circular component of
  the forecast balance. No forecast surplus will be called deliverable headroom.
- 2026-08-06: Added `pypdf==6.1.1` to `requirements.txt` to extract and inspect
  the official July STEO PDF. The reproducible builder itself uses only the
  standard library and the already-audited p2k.5 CSV.

### Source recovery

- Official July STEO report: <https://www.eia.gov/outlooks/steo/archives/jul26.pdf>.
  Pages 1 and 4-5 state that the June 18 U.S.-Iran MOU would open the Strait;
  EIA expected most crude production and trade patterns near pre-conflict levels
  by end-2026 and the majority of the remaining shut-ins back in 1Q27.
- Table 1 gives aggregate Gulf crude shut-ins of 8.290 mb/d in June, 5.427 mb/d
  in 3Q26, and 1.440 mb/d in 4Q26. Future country rows are intentionally blank;
  EIA only publishes the aggregate disruption forecast.
- Official July workbook:
  <https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx>. Its world
  production-minus-consumption path first turns positive in October 2026 at
  2.362 mb/d and averages +5.031 mb/d (+1,836.441 mb) in 2027.
- Official frozen-February workbook:
  <https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx>. It already
  projected a +2.680 mb/d 2027 surplus, but also projected 2027 demand 1.266
  mb/d above the July vintage.

### Missing public assumption and bound

The public report/workbook does **not** expose an exact monthly or country Gulf
shut-in path for 2027. The builder therefore bounds EIA's own average 2027
residual disruption at 0.000-0.898 mb/d. The upper edge is deliberately
conservative: retain all 1.440 mb/d through 1Q27, then retain half through
Q2-Q4. This implements only a bare majority returning by end-Q1 and assumes no
later backsliding. It is a project sensitivity, not a recovered EIA series.

### Result: what survives without reopening

| 2027 branch | Implied balance, mb/d | Volume, mb |
|---|---:|---:|
| Published July reopening path | +5.031 | +1,836 |
| Hold 3Q26 shut-ins; retain July demand | **-0.396 to +0.502** | **-144 to +183** |
| Same, but demand returns to frozen-February path | -1.661 to -0.764 | -606 to -279 |
| Hold June shut-ins; retain July demand | -3.259 to -2.361 | -1,189 to -862 |

The primary Q3-level no-reopening branch is generous: the 3Q average itself
follows the June opening and therefore already embeds improving traffic. Even
so, effectively zero of the published +5.031 mb/d survives. Its midpoint is
+0.053 mb/d, with a -0.396/+0.502 envelope. At most 0.502 mb/d can be labelled
a positive conditional balance at the optimistic edge, and even that is a
forecast flow rather than banked or assured absorption headroom.

The non-circular bridge is also informative. From 3Q26 to 2027 in the July
workbook, world supply rises 8.549 mb/d, demand rises 1.294 mb/d, and the balance
improves 7.255 mb/d. Removing 4.529-5.427 mb/d of embedded Gulf recovery leaves
only enough other supply growth to offset the starting 3Q deficit and demand
rebound approximately, not a durable five-million-barrel-per-day cushion.

### Artifacts and validation

- Builder: `scripts/build_p2k_9_forward_surplus_decomposition.py`
- Derived ledger: `data/derived/hormuz_p2k_9_forward_surplus_decomposition.csv`
- Validation: builder regenerated 36 unique rows; Python compilation passed;
  October is the first positive published month; primary no-reopening endpoints
  recompute to -0.395654/+0.501880 mb/d.

### Integration handoff

The durability document should publish the October 2026 crossover and the
+5.031 mb/d reopening-branch balance, then state immediately that only
-0.396 to +0.502 mb/d survives the primary no-reopening sensitivity. Replace
any blanket "zero forward surplus" wording with: **zero already-held buffer
credit; reopening branch +5.031 mb/d; continued-Q3-disruption branch roughly
balanced, with at most +0.502 mb/d optimistic conditional flow credit.**
