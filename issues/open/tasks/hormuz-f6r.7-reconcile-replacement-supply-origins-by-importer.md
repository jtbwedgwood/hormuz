---
id: "hormuz-f6r.7"
title: "Reconcile replacement supply origins by importer"
type: "task"
status: "open"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "importers"
  - "tradeflows"
  - "substitution"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: null
created_at: "2026-07-06T00:00:00Z"
updated_at: "2026-07-06T00:00:00Z"
---

# Reconcile replacement supply origins by importer

## Description

Tighten the country-by-country replacement-supply story for China, India, Japan, and South Korea. Distinguish named replacement origins, cargo rerouting, stock draw, demand destruction, and unresolved/other.

## Acceptance Criteria

- Country rows identify replacement origins where public evidence supports them.
- China section separates Russia, sanctioned/relabeled Iranian barrels, Saudi/UAE bypass barrels, commercial stocks, lower refinery runs, and unresolved/other.
- India section separates crude replacement from gas/LPG rationing and named LPG suppliers.
- Japan and South Korea get one-sentence replacement-origin/inventory-draw summaries suitable for the blog.
- Any cargo-level claim is flagged if it requires Kpler/Vortexa/licensed AIS rather than public data.

## Work Notes

- 2026-07-06: Filed from follow-up synthesis. Existing F6R tables provide adjustment buckets but not a fully reconciled origin-by-origin replacement matrix.
