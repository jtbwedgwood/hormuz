---
id: "hormuz-2y7.2"
title: "Define Strait of Hormuz transit geofence and counting rules"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "geospatial"
  - "shipping"
  - "tracker"
blocked_by:
  - "hormuz-fyp.1"
blocks:
  - "hormuz-2y7.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:23Z"
updated_at: "2026-07-06T15:00:00Z"
---

# Define Strait of Hormuz transit geofence and counting rules

## Description

Specify geofences, directionality, deduplication, anchorage/loitering treatment, and day-boundary logic for a daily ship transit count.

## Acceptance Criteria

Counting method distinguishes true transits from local movements; rules are testable and documented with edge cases.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocks: `hormuz-2y7.4` - Prototype daily transit count pipeline

## Work Notes

- 2026-07-06: Claimed. First-pass geofence/counting methodology delegated to subagent Confucius. Provisional approach is to define a reproducible crossing-line method, then validate line placement against AIS samples and external daily/weekly traffic benchmarks.
- 2026-07-06: Methodology pass from Confucius. Core unit should be one deduplicated vessel track crossing event, not AIS ping counts. Canonical daily assignment should use UTC crossing timestamp interpolated at the primary gate. Narrative/local-day sensitivity can be UTC+4, but canonical UTC avoids mixing Oman/UAE UTC+4 with Iran UTC+3:30.

### Provisional Count Method

Count a transit when:

1. A vessel track crosses the primary Strait throat gate.
2. The same track has plausible evidence connecting the Gulf of Oman side and Persian Gulf side within an initial 48-hour window.
3. Speed, course, and time gaps do not imply impossible movement.
4. The vessel belongs to the target merchant fleet for the headline series. Keep fishing, pleasure, military/law-enforcement, pilot boats, local tugs, and small craft in a separate observed-AIS layer.

Direction:

- `inbound_to_gulf`: movement from Gulf of Oman side to Persian Gulf side.
- `outbound_from_gulf`: movement from Persian Gulf side to Gulf of Oman side.
- `ambiguous`: crossing observed but side evidence conflicts or is missing.

### Draft Geometries To Validate

Draft primary throat gate: `(26.24, 56.50)` to `(26.56, 56.50)`.

Draft confirmation boxes:

| Geometry | Bounds |
|---|---|
| `HORMUZ_CORE` | `lat 26.20-26.58`, `lon 56.20-56.75` |
| `GULF_OF_OMAN_SIDE` | `lat 25.60-26.80`, `lon 56.65-57.45` |
| `PERSIAN_GULF_SIDE` | `lat 25.75-26.65`, `lon 54.30-56.15` |
| `TUNB_FARUR_CONFIRM` | `lat 26.05-26.40`, `lon 54.30-55.55` |

These are methodological placeholders. Validate against IMO routeing coordinates, ENC/chart layers, and real AIS samples before publication. Public anchors: IMO Resolution A.284(VIII) routeing/TSS coordinates, NGA Pub. 172 sailing directions, EIA Strait explainer, and IMO AIS carriage rules. Sources: https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.284%288%29.pdf, https://maritimesafetyinnovationlab.org/wp-content/uploads/2021/04/NGA-Sailing-Directions-Pub-172-Red-Sea-and-The-Persian-Gulf.pdf, https://www.eia.gov/todayinenergy/detail.php?id=4430, https://www.imo.org/en/ourwork/safety/pages/ais.aspx.

### Deduplication And Edge Rules

- Reconcile identity by MMSI first, then IMO/callsign/name/dimensions/type where available.
- Split tracks with impossible movement, initially `>60 kn` for merchant vessels unless vessel-specific thresholds are justified.
- Merge repeated same-gate/same-direction crossings within 6 hours when caused by jitter, sparse interpolation, or loitering.
- Count a second transit only after the vessel reaches the opposite-side confirmation box or completes a credible round trip.
- Quarantine invalid/common-placeholder/duplicated MMSIs and physically impossible shared-MMSI tracks. Source for MMSI/AIS identity risks: https://www.navcen.uscg.gov/ais-frequently-asked-questions.
- Classify vessels entering the core and returning to the same side without opposite-side evidence as `local_or_aborted`.
- Flag rather than discard sparse-AIS inferred crossings, AIS-dark gaps, outside-TSS routing, anchoring/loitering, and possible spoofing/GNSS anomalies. AIS spoofing/anomaly risks source: https://www.mdpi.com/2076-3417/11/11/5015.

### Why Ping Counts Are Invalid

Raw AIS message/ping counts are biased by vessel transmission frequency, speed, AIS class, receiver density, satellite pass timing, duplicate receivers, anchoring/loitering, dark ships, spoofing/jamming, MMSI errors, and provider processing. Daily tracker must be based on deduplicated vessel crossing events.

### Closeout

- This method remains the correct specification if raw AIS is later obtained.
- For the current public-only tracker, the operational boundary/counting method is IMF PortWatch's chokepoint method rather than our own custom geofence. The blog should say "PortWatch chokepoint calls," not "our vessel-level AIS crossing count."
