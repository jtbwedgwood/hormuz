---
id: "hormuz-p2k.13"
title: "Test whether rerouting actually caused the oil-on-water rise"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "oil-on-water"
  - "causal-test"
  - "historical-comparison"
blocked_by: []
children: []
blocks: []
owner: "p2k13_rerouting_test"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T21:30:00Z"
---

# Test whether rerouting actually caused the oil-on-water rise

## Description

`hormuz-p2k.12` establishes **how much** oil moved onto water. This issue tests **why**, and
exists specifically because the project has been asserting the rerouting explanation without
evidence.

The working hypothesis is that longer voyages caused by the Hormuz disruption mechanically
increased the barrels required to be in transit at any moment: Petroline to Yanbu and onward
to Asia is a far longer haul than a Hormuz transit, and the IEA separately reported roughly
3.5 mb/d of additional Atlantic Basin crude moving East of Suez, among the longest routes in
the trade. Under that hypothesis the oil-on-water rise is a **cost** of the disruption, not a
buffer, and is unavailable to consumers.

That is plausible and mechanically sound. **It is also unverified, and at least five other
mechanisms would produce the same observed signature.** Do not treat it as established, and do
not assume it accounts for the whole increase even if it is confirmed as a contributor.

## Competing mechanisms to test, not assume

1. **Voyage-length inflation from rerouting.** The working hypothesis.
2. **Discretionary floating storage.** Cargoes deliberately held offshore. Near-certainly the
   dominant mechanism for the March Gulf build, when exports were physically blocked and
   loaded tankers had nowhere to discharge.
3. **Discharge-port congestion.** Vessels queueing to unload count as on water without being
   either voyage float or deliberate storage.
4. **Sanctioned and dark-fleet accumulation.** A pre-existing trend independent of Hormuz: the
   IEA reported oil on water rising 248 mb across 2025 with about 72% of it sanctioned oil.
   Some of the 2026 increase may be continuation of that trend rather than shock response.
5. **Pipeline refill after the June partial reopening.** When flows restart, the transit
   system refills. This is distinct from voyage lengthening and is specific to June.
6. **Measurement and classification change.** AIS coverage, dwell-time thresholds, geographic
   reassignment and revisions to voyage classification. The project data already references
   "revisions to voyage classification" as a known factor.

## Proposed tests

### A. Ton-mile arithmetic

Barrels in transit approximate to `delivery rate x average voyage days`. Estimate the change
in average voyage days implied by the observed route shift and convert to barrels.

As an illustrative sanity check only: roughly 3.5 mb/d shifting from a Persian Gulf to Asia
voyage of about 18-22 days to a US Gulf or Atlantic Basin to Asia voyage of about 45-50 days
implies roughly 25-30 additional transit days, or on the order of 95 mb of additional
permanent float. That is the right order of magnitude to matter, which is why the test is
worth doing properly. **These voyage-day figures are unverified placeholders and must be
replaced with sourced route distances and realistic laden speeds.**

If the computed float increase materially undershoots the observed rise, rerouting is not the
whole story and the remainder needs another mechanism.

### B. Price-structure discriminator

This may be the single cleanest test. Discretionary floating storage is only profitable in
**contango**, where deferred prices exceed prompt. A shortage normally produces
**backwardation**, which penalizes holding oil at sea.

So: if the market was in backwardation while oil on water was rising, mechanism 2 is largely
excluded and the increase is far more likely voyage float or congestion. If it was in
contango, discretionary storage becomes a live competitor to the rerouting story.

This requires time-spread data the project does not currently hold; it overlaps
`hormuz-r3v.3` / `hormuz-p2k.3` on price series and should be coordinated with whichever of
those runs first.

### C. Geographic decomposition

Where the oil sat is diagnostic. Increases concentrated in **transit lanes** (Indian Ocean,
around the Cape, Red Sea approaches) support voyage float. Increases concentrated at
**loading anchorages** near Gulf terminals support blocked-export storage, which is the
expected March signature. Increases at **discharge ports** in Asia support congestion.

The March and June cases likely have different dominant mechanisms, and geography should show
it. A finding that they differ would be a genuine result, not a complication.

### D. Historical analogues

Two clean routing-driven precedents and one clean storage-driven control:

- **2022 Russian sanctions and rerouting.** Russian crude redirected from Europe to India and
  China caused a large, well documented ton-mile increase with no comparable production loss.
  The closest available analogue for a pure routing effect on oil on water.
- **2024 Red Sea and Houthi diversions.** Traffic shifted from Suez to the Cape of Good Hope.
  Also a near-pure routing change, and the diverted volumes and added voyage days are
  publicly documented.
- **2020 COVID contango.** Oil on water spiked for the opposite reason: deliberate floating
  storage in deep contango. Useful as a **negative control** — it shows what a
  storage-driven spike looks like, so the 2026 signature can be compared against both
  patterns rather than only against the hypothesis being tested.

For each, recover the volume rerouted, the added voyage days, and the resulting change in oil
on water, then compare the implied barrels-per-added-voyage-day ratio with 2026.

## Acceptance Criteria

- A quantified estimate of the voyage-float component from sourced route distances and
  speeds, with the illustrative figures in this issue replaced.
- An explicit verdict on how much of the March-June oil-on-water increase rerouting explains,
  with a range, and what the remainder is attributed to.
- The price-structure test run, or its unavailability documented as blocking.
- Geographic decomposition attempted, with March and June treated as potentially different
  mechanisms rather than forced into one explanation.
- At least the 2022 and 2024 analogues quantified and compared like-for-like, with 2020 used
  as a contrasting storage-driven case.
- Sanctioned-fleet and dark-fleet continuation explicitly netted out or bounded, so the
  pre-existing 2025 trend is not misattributed to Hormuz.
- A clear statement of what remains unidentified. Partial attribution with an honest remainder
  is the expected outcome; a single-cause conclusion should be treated as suspicious.

## Notes

Watch for the same over-refusal failure mode flagged in `hormuz-p2k.8`. A bounded estimate
with stated assumptions beats declining to compute. If route distances are uncertain, publish
the calculation across a range of assumed voyage days rather than reporting "unknown."

Also note the finding cuts two ways simultaneously and both should be reported together: a
larger voyage-float component means **less accessible buffer remained** (durability worse) but
also **a smaller unreconciled residual** (accounting cleaner). These are not in tension; they
are the same barrels seen from two sides.

## Source Leads

- IEA Oil Market Reports March-July 2026, oil-on-water and floating-storage commentary
- IEA readjustment commentary on Atlantic Basin crude moving East of Suez
- Kpler and Vortexa published methodology on floating-storage dwell-time thresholds
- IEA and trade coverage of 2024 Red Sea diversions and 2022 Russian crude rerouting
- IMF PortWatch chokepoint transit data for route-share change: `data/external/portwatch/`
- `data/derived/hormuz_m8q_1_monthly_oil_balance.csv` and `hormuz_m8q_3_global_adjustment_evidence.csv`

## Work Notes

- 2026-08-06: Claimed by `p2k13_rerouting_test`. Work is proceeding on the independent ton-mile arithmetic and historical controls while `hormuz-p2k.12` constructs the authoritative March-June oil-on-water denominator. The final attribution will retain a denominator sensitivity rather than pretending the dependency is already resolved.
- 2026-08-06: Built `scripts/build_p2k_13_rerouting_causal_test.py` and `data/derived/hormuz_p2k_13_rerouting_causal_test.csv` (23 rows, 28 fields). The builder validates unique IDs and all headline arithmetic.
- 2026-08-06: Replaced the issue's unsourced illustrative calculation with three explicit route cases, all using EIA's public 14-knot laden-speed convention and transparent voyage-day/distance envelopes:
  - IEA's observed 3.5 mb/d Atlantic-to-East-of-Suez shift adds **42/70/98 mb** of structural voyage float at 12/20/28 extra days (4,032/6,720/9,408 nautical miles).
  - The lower-bound 3 mb/d increment in Yanbu exports above the 2 mb/d pre-war level adds **15/21/27 mb** at 5/7/9 extra days (1,680/2,352/3,024 nautical miles). This is limited to the increment and carries a destination-mix caveat.
  - June Hormuz traffic refill is separate from rerouting. The `p2k.2` 5.5/6.2/6.9 mb/d increase versus the March-May average adds **66/111.6/151.8 mb** of ordinary working float at 12/18/22 laden days. This is the main explanation for June, but is not longer-route inflation.
- 2026-08-06: Strict structural rerouting is therefore **57/91/125 mb** at the end-June route mix. Structural rerouting and ordinary June refill are not automatically additive across time: the former may have accumulated before June and may unwind as Gulf flows return. A conditional end-June snapshot in which both remain gives 123/202.6/276.8 mb, retained only as a scale check.
- 2026-08-06: Reconciled to `p2k.12`'s final monthly denominator. Global oil on water changed **-117 mb in March, +53 mb in April, unknown in May, and +117 mb in June**. With May bounded at -35/0/+35 mb, the March-June net change is only **+18/+53/+88 mb**, not 270 mb. The issue's original +100 mb March number is regional Middle East Gulf floating storage nested inside the -117 mb global change.
  - March's geography is the clearest rejection of a one-mechanism story: the revised bridge is -181 mb in-transit, +100 mb Middle East floating storage and -36 mb other/vintage = -117 mb global oil on water. Blocked storage rose near loading points while the global maritime pipeline drained.
  - June's +117 mb can be paired with 66/111.6/151.8 mb of ordinary route refill and a +51/+5.4/-34.8 mb discretionary-or-other remainder. The upper-refill case implies some blocked storage was simultaneously released. The unexplained June net remainder is therefore a **51 mb build to a 35 mb unwind**, with a **5.4 mb base build**.
  - Accounting guardrail: the oil-on-water series closes **zero** barrels of the supply-demand residual on a valid same-boundary comparison because oil on water is already inside IEA total observed stocks. Reclassifying it is useful for accessible-headroom/durability analysis; adding it again to total draws is double counting.
- 2026-08-06: Price-structure test completed using the refreshed `r3v.3` time-spread artifact. March-June WTI was backwardated on 84/84 observed days (front-minus-December mean +$15.943/b); Brent was backwardated on 82/84 (mean +$15.037/b). This strongly rejects profit-seeking contango carry as a major explanation, but does not reject forced blocked cargoes, congestion, sanctioned dwell or voyage float.
- 2026-08-06: Historical order-of-magnitude controls:
  - 2022 Russia: the named India and China increase of 1.19 mb/d implies 29.75/35.7/41.65 mb at 25/30/35 extra days; IEA's broader approximate 2.5 mb/d eastward displacement implies 62.5/75/87.5 mb. UNCTAD independently reports global crude ton-miles up 8% in 2022. No public like-for-like global oil-on-water series exists, so this validates scale, not a calibration coefficient.
  - 2024 Red Sea: EIA's 2.8 mb/d increase in Cape oil flows and representative 15-day detour implies 28/42/58.8 mb across 10/15/21 days. Again this is an order-of-magnitude route control, not a direct observed oil-on-water attribution.
  - 2020 negative control: IEA's May crude floating-storage peak is recoverable as 211.3 mb; it fell 34.9 mb in June as contango flattened. This is the expected signature of profitable storage and differs from persistent 2026 backwardation.
- 2026-08-06: Explicitly bounded competing mechanisms rather than assigning all residual to rerouting. Straight-lining the 2025 +248 mb oil-on-water trend gives an intentionally loose four-month hard cap of 82.67 mb (59.52 mb sanctioned-only); the recommended 0/30/82.67 mb range is non-additive because sanctioned barrels themselves use longer routes. Congestion is retained only as an unsupported 0-30 mb sensitivity, and May measurement/classification at -35/0/+35 mb.
- 2026-08-06: Verdict: **rerouting is sufficient to explain the small net +53 mb period rise, but a percentage of the net is not identified because gross route float, normal refill, blocked-storage accumulation/release and March pipeline drainage offset one another.** The strongest bounded claim is that strict longer-route inflation required 57-125 mb by end June, while ordinary route refill can explain 66-117 mb (56-100%; base 95%) of June's net +117 mb. Vessel-level cargo state, anchorage geography, dwell thresholds and discharge-port queues remain unidentified. This partial attribution with an honest remainder meets the acceptance criteria without treating the price signal as dispositive.
