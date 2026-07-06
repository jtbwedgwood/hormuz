---
id: "hormuz-2y7.8"
title: "Vessel-level paid AIS crossing reconstruction"
type: "task"
status: "deferred"
priority: "P2"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "commercial-data"
  - "deferred"
  - "shipping"
  - "tracker"
blocked_by:
  - "no-paid-ais-access"
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T15:00:00Z"
updated_at: "2026-07-06T16:00:00Z"
---

# Vessel-level paid AIS crossing reconstruction

## Description

Build and validate a vessel-level Strait of Hormuz crossing reconstruction from raw historical AIS positions, including direction, individual vessel identity, duplicate/identity handling, and track-level confidence flags.

## Acceptance Criteria

Historical raw AIS positions are available for the Hormuz crossing area; pipeline produces auditable vessel-level crossing events with vessel ID, direction, timestamp, vessel class, and confidence flags; counts reconcile with public PortWatch and spot-check benchmarks.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `no-paid-ais-access` - User decided not to spend $200+ on commercial ship-tracker data for this blog-post scope.

## Work Notes

- 2026-07-06: Deferred by scope/cost decision. Public PortWatch is sufficient for aggregate daily traffic, but it does not expose vessel identities, direction, exact gate-crossing tracks, AIS-dark diagnostics, or onboard cargo.
- Free alternatives do not fully solve this: Global Fishing Watch AIS Vessel Presence is hourly/thinned presence, not raw vessel tracks; AISstream is live-only and has no historical backfill.
- Reopen only if a free institutional license appears or the blog explicitly needs vessel-level auditability enough to justify commercial AIS access.
