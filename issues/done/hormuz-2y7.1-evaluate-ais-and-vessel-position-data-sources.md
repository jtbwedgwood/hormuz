---
id: "hormuz-2y7.1"
title: "Evaluate AIS and vessel-position data sources"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "data-sources"
  - "shipping"
  - "tracker"
blocked_by:
  - "hormuz-fyp.1"
blocks:
  - "hormuz-2y7.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:21Z"
updated_at: "2026-07-06T15:00:00Z"
---

# Evaluate AIS and vessel-position data sources

## Description

Compare accessible sources for historical AIS or vessel movement data, including MarineTraffic, Spire, exactEarth, Kpler/Vortexa, AIS aggregators, port call data, and public alternatives.

## Acceptance Criteria

For each source, record coverage, history depth, cost/access, API/export options, vessel fields, redistribution limits, and expected bias.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocks: `hormuz-2y7.4` - Prototype daily transit count pipeline

## Work Notes

- 2026-07-06: Claimed. First-pass provider evaluation delegated to subagent Peirce. Proceeding with a provisional source-quality standard: prefer provider documentation, official data portals, peer-reviewed/published methodology, then clearly attributed analyst/news snapshots; flag paywalled/redistribution constraints explicitly.
- 2026-07-06: First-pass source ranking from Peirce:
  - Best no-enterprise prototype path: Global Fishing Watch AIS Vessel Presence for historical public hourly vessel-presence signals plus AISstream.io for live-forward capture. This is not a perfect exact transit ledger because GFW thins/grids AIS and AISstream is live-only, but it is the most reproducible path without paid access. Sources: https://globalfishingwatch.org/our-apis/documentation, https://globalfishingwatch.org/platform-update/global-ais-vessel-presence-dataset/, https://globalfishingwatch.org/faqs/can-i-use-global-fishing-watch-apis-for-commercial-purposes/, https://aisstream.io/documentation.
  - Best raw AIS path if funding/access exists: MarineTraffic/Kpler AIS. MarineTraffic docs indicate historical positions since January 2015; Kpler markets 10+ years of historical AIS and multiple delivery formats. Likely paid/contracted, with redistribution limits and query constraints. Sources: https://servicedocs.marinetraffic.com/tag/Vessel-Historical-Track/, https://www.kpler.com/product/maritime/kplerais, https://www.kpler.com/product/maritime/data-services.
  - Spire/exactEarth should now be evaluated mainly through Kpler because legacy Spire docs show discontinuation/migration after acquisition. Useful institutional archives may exist but are not a clean current procurement path. Sources: https://servicedocs-sm.kpler.com/historical-positions-api/, https://docs.meroxa.com/sources/spire-maritime-ais/.
  - Best commodity-flow complement, not raw all-ship tracker: Vortexa or Kpler commodity products. Vortexa is strong for oil/products/LNG cargo movements and volumes, likely enterprise access. Sources: https://www.vortexa.com/product/integrations/energy-data-api-integration, https://www.vortexa.com/feature/energy-flow-analytics-cargo-tracking.
  - Enterprise alternatives for high-quality validation/access if institution has licenses: ORBCOMM/S&P Maritime Portal, Lloyd's List Intelligence/Seasearcher/AIS SeaOrbis. Sources: https://api.commtrace.com/, https://www.spglobal.com/market-intelligence/en/solutions/products/maritime-ship-tracker-ais-live-ship-data-seaweb, https://www.lloydslistintelligence.com/solutions/seasearcher, https://www.lloydslistintelligence.com/solutions/ais-seaorbis.
  - Budget/self-serve paid pilots for coverage tests: VesselFinder, Datalastic, Searoutes. Validate Hormuz coverage, history depth, API export, and redistribution before relying on them. Sources: https://www.vesselfinder.com/historical-ais-data, https://api.vesselfinder.com/docs/, https://datalastic.com/api-reference/, https://searoutes.com/vessel-api/.
  - Validation supplement: IMF PortWatch/UN AIS-derived aggregates may provide chokepoint or port-call sanity checks, but not raw vessel positions. Confirm whether Hormuz is exposed in its public catalog/API. Sources: https://portwatch.imf.org/pages/data-and-methodology, https://portwatch.imf.org/api/search/definition/.

### Provisional Evaluation Table

| Source | Access | History | Fit for daily Hormuz tracker | Main caveat |
|---|---|---:|---|---|
| Global Fishing Watch AIS Vessel Presence | Public API, non-commercial/public-good use | 2012 to near-real time lag | Best public prototype / validation proxy | Hourly standardized presence, not raw tracks |
| AISstream.io | Free live WebSocket | Live only | Build forward archive | No historical backfill; coverage must be tested |
| MarineTraffic/Kpler AIS | Paid API/enterprise | MT docs: since 2015; Kpler markets 10+ years | Best rigorous raw AIS tracker | Contract, redistribution, query limits |
| Vortexa/Kpler commodity flows | Enterprise | Multi-year energy/cargo history | Best cargo disruption complement | Not all-vessel transit count |
| ORBCOMM/S&P, Lloyd's/Seasearcher | Enterprise | Not clearly public | Potential high-quality validation/source | Heavy procurement |
| VesselFinder/Datalastic/Searoutes | Paid/self-serve-ish | Varies by provider | Pilot/spot-check option | Coverage and licensing uncertainty |

### Open Questions

- Resolved for current scope: user does not want to spend $200+ on paid trackers, so Kpler/MarineTraffic/VesselFinder/Datalastic/S&P/Lloyd's/Vortexa are not active paths.
- Resolved: IMF PortWatch exposes a Hormuz chokepoint series suitable for public daily validation/backfill.
- Remaining caveat: GFW may still be useful as a public AIS-presence sensitivity check, but it is not needed to finish the public tracker.

### Closeout

- Decision: use IMF PortWatch as the primary public daily tracker and source of truth for broad vessel-class transit calls.
- Paid AIS is no longer pursued for this blog-post scope. The paid/raw vessel-level reconstruction path is captured separately as blocked issue `hormuz-2y7.8`.
