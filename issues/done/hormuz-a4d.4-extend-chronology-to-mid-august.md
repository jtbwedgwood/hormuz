---
id: "hormuz-a4d.4"
title: "Extend the chronology to mid-August and verify the July re-closure narrative"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-a4d"
labels:
  - "chronology"
  - "verification"
  - "blog"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T00:00:00Z"
---

# Extend the chronology to mid-August and verify the July re-closure narrative

## Description

`docs/foundation-chronology-and-scenarios.md` was last updated **2026-07-06** and its "current
read" is the fragile-partial-reopening regime. The draft's opening and closing paragraphs make
three claims about events **after** that cutoff, none of which the repo currently sources.

Claims to verify or correct:

1. **"Full closure resumed in July in response to US violations of the memorandum of
   understanding."** Two separate problems. (a) Magnitude: PortWatch shows 2026-07-08 onward
   at ~11.7% of baseline total calls, which is a severe re-closure but not the near-zero of
   early March (4 calls on 2026-03-07); meanwhile the repo's own note records the IEA saying
   on 21 July that Gulf exports "slipped below late-June highs but remained above early-March
   to mid-June levels." Establish which metric supports which wording. (b) Attribution: the
   repo documents a 7-8 July escalation but has **no source** for the claim that US violations
   of the 17 June memorandum caused it. Find one or rewrite the sentence.
2. **"Iran has recently issued a list of maximalist demands for reopening the Strait."** No
   repo source. Date it, source it, and summarise the actual demands.
3. **The 60-day clock from the 2026-06-17 agreement expires 2026-08-16**, two days before the
   stated writing date. Establish what happened at expiry; this is the natural hook for the
   draft's "no clear end in sight" framing and is currently absent.

Also extend the chronology table with: post-06-July UKMTO/JMIC advisories and threat levels,
the July escalation, OPEC+ August/September decisions, and the current traffic-state
officialdom. Update the "Current Read" and the S6 scenario's best-fit assessment.

## Acceptance Criteria

- Chronology table extended to the publication date with the project's confidence labels.
- Each of the three draft claims above is either sourced or has replacement wording proposed.
- "Current Read" paragraph rewritten for mid-August, replacing the 2026-07-06 framing.
- If the 60-day clock lapsed without settlement, that is recorded as a dated event.

## Dependency Notes

- Parent: `hormuz-a4d`

## Work Notes

- Existing anchors: 2026-06-17 US-Iran agreement (AP, CFR); 2026-06-26/27 escalation
  (Euronews via UKMTO/CENTCOM); 2026-07-02 and 07-05 traffic/governance (Guardian);
  OPEC+ 188 kb/d August increase (WSJ).
- 2026-08-18: Claimed for primary-source and reputable-wire verification through the stated
  writing date. Scope is the canonical chronology/current-read document only; PortWatch and
  tracker artifacts remain owned by `hormuz-a4d.3`.
- 2026-08-18: Updated `docs/foundation-chronology-and-scenarios.md` through 18 August with
  eleven new dated rows: the 7 July tanker strike, 10 July competing violation claims, 14 July
  JMIC risk/legal-transit assessment, 20 July tanker abandonment, 2 August OPEC+ decision,
  early-August Iranian conditions, 11 August STEO baseline, 12 August IEA July-flow estimate,
  15 August ship attack, 17 August deadline outcome and 18 August traffic/diplomacy state.
- Claim 1 disposition: **corrected, not sourced as written.** UKMTO confirms attacks on 7
  and 20 July; JMIC's 14 July advisory rates the Strait `SEVERE` but explicitly says neutral
  transit remains permitted. AP's retrospective says Iran attacked vessels on the
  U.S.-overseen Omani route, the U.S. responded and restored the blockade, and both sides
  accused the other of violating the memorandum. Recommended wording is a failed June
  reopening followed by severe, controlled residual transit after reciprocal escalation;
  do not assign sole causation to U.S. violations.
- Claim 2 disposition: **sourced and made concrete.** AP's 17 August deadline assessment
  reports Iran's early-August conditions: lift the U.S. blockade, withdraw U.S. forces from
  around Iran, pay war reparations, and accept an Iranian management role/possible fees.
  State the conditions; treat "maximalist" as interpretation.
- Claim 3 disposition: **deadline passed without agreement.** AP reports Pakistan treated
  Monday 17 August as the operational deadline. No permanent settlement or extension was
  announced, no Strait compromise was evident, and AP found no sign detailed nuclear talks
  had begun. This authoritative event date resolves the issue's arithmetic 16 August date.
- Current-state synthesis: 14 July is the latest located comprehensive JMIC advisory and
  remains the official maritime-risk anchor (`SEVERE` Strait, `SUBSTANTIAL` Gulf of Oman,
  neutral transit permitted). AP reported on 18 August that Kpler counted 95 crossings in
  the latest week (-19.5%), only three on 16 August, all through the Iranian-designated
  route and none through Omani routes. Accordingly S2 managed partial closure plus S1
  security shock replaces S6 as the current best fit; S6 is retained as an upside branch.
- OPEC+ verification: official OPEC releases confirm separate 188 kb/d production
  adjustments for August (decided 5 July) and September (decided 2 August). The 2 August
  JMMC statement stresses safeguarding maritime routes and infrastructure-repair lags.
  These are target decisions, not evidence that shut-in/export-constrained barrels flowed.
- Verification: all 23 source URLs in the chronology through the new rows were checked on
  18 August. EIA, IEA, OPEC, AP and other HTML sources returned HTTP 200. UKMTO PDFs and WSJ
  returned HTTP 403 to command-line requests but were discoverable/readable through indexed
  web results; the added UKMTO/JMIC content was checked against the official PDF text.
  A structural check confirms every dated chronology row retains six fields, and the
  updated file contains the 18 August current read, 17 August deadline row and revised S6
  assessment. No tracker file or artifact was edited.
