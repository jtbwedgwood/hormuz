---
id: "hormuz-a4d.7"
title: "Verify two unsourced draft claims: the IEA superlative and the Red Sea blockade"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-a4d"
labels:
  - "verification"
  - "citations"
  - "blog"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T16:15:00-06:00"
---

# Verify two unsourced draft claims: the IEA superlative and the Red Sea blockade

## Description

Two claims in the blog draft have **no support anywhere in this repo** and both are
load-bearing enough to be worth a dedicated check.

1. **"the 'largest supply disruption in the history of the global oil market' by the IEA."**
   The repo has a verified IEA superlative, but it is a different one: the 11 March 2026
   announcement of the *largest ever collective oil stock release*. A disruption superlative
   is a stronger and separate claim, and `docs/hormuz-historical-comparison.md` actively
   argues the opposite framing — that on crude alone the shock does **not** outrank the 1970s
   once duration, bypass, stocks and demand response are normalised. Either find the exact
   IEA wording and date, or replace the sentence. If the IEA did say it, note whether it was
   scoped to a rate (mb/d removed) rather than to overall severity, and keep the historical-
   comparison caveat nearby so the post does not contradict itself.

2. **"Saudi Arabia's oil is now blockaded in Bab al-Mandeb."** This would be a major finding
   and it cuts directly against the repo's core supply-side story. Petroline delivers to
   Yanbu on the Red Sea; Yanbu exports above 5 mb/d in early June are the largest single
   component of the 362 mb incremental bypass. If Bab al-Mandeb were blockaded, southbound
   Asia-bound Yanbu cargoes would be constrained and the bypass credit would need revision.
   The repo's only Bab al-Mandeb references are to the **2024** Red Sea disruptions. Determine
   whether there is a 2026 Bab al-Mandeb interdiction, how much Saudi flow it actually
   affects, and whether Suez-northbound routing absorbs it. If it is real, it belongs in the
   bypass durability analysis (`hormuz_p2k_7_bypass_headroom_vulnerability.csv`), not only in
   a regional-impacts aside.

## Acceptance Criteria

- Each claim marked verified-with-citation, corrected, or dropped, with proposed wording.
- If claim 2 is real, a quantified effect on the 362 mb incremental bypass estimate and on
  the bypass-headroom vulnerability analysis.
- If claim 1 is real, a note reconciling it with `docs/hormuz-historical-comparison.md`.

## Dependency Notes

- Parent: `hormuz-a4d`

## Work Notes

- 2026-08-18: Claimed for primary-source verification of the IEA disruption
  superlative and the alleged 2026 Bab al-Mandeb blockade. Scope includes proposed
  blog wording and changes to the historical-comparison or bypass analysis only if
  the evidence warrants them.

### Claim 1: verified, with a peak-physical-volume scope

- The exact IEA wording is real: **“the largest supply disruption in the history of the
  global oil market.”** The earliest directly located IEA use is its 15 March collective-
  action update:
  https://www.iea.org/news/update-on-iea-collective-action-decision-of-11-march-2026
- The IEA's 20 March *Sheltering From Oil Shocks* report supplies the comparison rule. It
  says the **volume of fuel supply offline** exceeded the 1973 loss and every disruption
  since. At that point, roughly 15 mb/d of crude and 5 mb/d of products normally crossing
  Hormuz had slowed to a trickle, while Gulf countries had cut production by at least
  10 mb/d. Source:
  https://www.iea.org/reports/sheltering-from-oil-shocks/introduction-and-context
- This is a peak-flow/offline-volume superlative, not an all-dimensional historical severity
  ranking. Duration, cumulative loss, bypasses, inventories, demand response, prices and
  affected product mix remain separate comparison dimensions.
- Proposed blog wording: **“The IEA calls this the largest oil-supply disruption in history
  by peak physical volume: it says the amount of fuel offline exceeded 1973 and every
  disruption since. That does not make it automatically the most severe shock after
  duration, bypasses, stocks and demand response are considered.”**
- Updated `docs/hormuz-historical-comparison.md` to include the exact attribution, date,
  metric scope and reconciliation. This resolves the apparent conflict with the document's
  warning against a context-free “biggest shock ever” claim.

### Claim 2: corrected; real selective interdiction, not a sealed chokepoint

- On **20 July**, the Houthis declared an immediately effective maritime embargo against
  vessels serving Saudi ports and said Bab el-Mandeb was closed to Saudi-linked shipping.
  The UK government described this on 21 July as **plans to impose** a maritime blockade,
  not an internationally recognized closure:
  https://www.gov.uk/government/news/fcdo-statement-on-houthi-threats-against-saudi-arabia
- JMIC's 21 July advisory gives the crucial status distinction: traffic continued steadily,
  no merchant attack had been confirmed in the prior 48 hours, no routing changes were yet
  observed, and Bab el-Mandeb/Southern Red Sea remained `MODERATE`, even as JMIC recorded
  the Houthi proclamation. Source:
  https://www.ukmto.org/-/media/ukmto/products/update-074-jmic-advisory-note-21-july.pdf
- Enforcement later became real but selective. AP reported Houthi claims of attacks on two
  Saudi oil tankers on 23 July and a deadly 11 August missile attack on a Yemeni commercial
  vessel in Bab el-Mandeb. Traffic never stopped, some Saudi cargoes transited with AIS dark,
  and other cargoes were redirected north. Sources:
  https://apnews.com/article/896c02f0c978986fff0ae7fc389ea51f and
  https://apnews.com/article/iran-us-strait-hormuz-august-11-2026-91e4efdfe1ac035b2065127550377289
- Kpler's post-declaration factbox observed continued Saudi crude transits and continued
  Yanbu terminal draw/loading. Its separate outlook estimated roughly **3 mb/d** could be
  diverted north via Suez/SUMED, though Yanbu-South Korea transit would roughly double from
  **24 to 54 days**. Sources:
  https://www.kpler.com/blog/factbox-red-sea-crude-flows-bab-el-mandeb-and-alternative-routes
  and https://www.kpler.com/fr/blog/update-middle-eastern-supply-recovery-postponed-to-early-2027
- Reuters/Kpler data on 30 July put the southbound share of Yanbu loadings at **43%**, down
  from **81% in June**, while northbound Sidi Kerir/SUMED use rose. This is strong evidence
  of routing friction, but AIS-dark movements and missing matched total loadings prevent a
  defensible net-supply haircut. Source:
  https://www.internazionale.it/ultime-notizie-reuters/2026/07/30/analysis-drone-strike-in-egypt-sparks-security-concerns-about-suez-oil-exports
- Proposed blog wording: **“Since 20 July, the Houthis have declared and partly enforced a
  Saudi-specific maritime embargo at Bab el-Mandeb, attacking shipping and sharply reducing
  visible southbound Yanbu traffic. The strait is not sealed: some cargoes still pass and
  Saudi Arabia is shifting others north through Suez and SUMED, at materially higher cost
  and transit time.”** Drop **“Saudi Arabia's oil is now blockaded in Bab al-Mandeb.”**

### Accounting and artifact treatment

- The **362.1 mb March-June bypass estimate is unchanged**: the Houthi declaration began on
  20 July, outside that historical frame. The approximately 3.4 mb/d June net increment
  also cannot be multiplied by a change in visible southbound traffic shares; Yanbu loading,
  Bab el-Mandeb transit, northbound rerouting, AIS darkness and delivered supply have
  different boundaries.
- Updated `scripts/build_p2k_7_bypass_headroom_vulnerability.py` and regenerated
  `data/derived/hormuz_p2k_7_bypass_headroom_vulnerability.csv` with a sixth, non-additive
  realized-interdiction row. Updated the manifest and
  `docs/hormuz-shock-absorption-durability.md`. The row preserves the historical total and
  records the forward risk as delivery delay, destination constraint, insurance cost and
  potential stepwise loss—not a fabricated barrel haircut.
- Validation: the builder compiles and runs under `.venv`; the regenerated CSV has six
  unique rows; the new context row contains the historical-period guardrail and the observed
  43%/81% route-share evidence. Both claims now have a verdict, exact proposed wording and
  primary/first-party source breadcrumbs. Acceptance criteria met.
