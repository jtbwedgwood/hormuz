---
id: "hormuz-f6r.2"
title: "Analyze China exposure and substitution behavior"
type: "task"
status: "open"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "china"
  - "importers"
  - "imports"
  - "tradeflows"
blocked_by:
  - "hormuz-f6r.1"
  - "hormuz-kmz.3"
blocks:
  - "hormuz-f6r.5"
  - "hormuz-s49.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:43Z"
updated_at: "2026-07-06T06:09:43Z"
---

# Analyze China exposure and substitution behavior

## Description

Estimate China's exposure to Hormuz crude, LNG, LPG, petrochemicals, and fertilizers, then examine substitution via Russia, domestic inventories, demand reduction, refinery runs, or SPR/commercial draws.

## Acceptance Criteria

China section separates observed data from inference and flags opaque inventory assumptions.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Blocked by: `hormuz-f6r.1` - Build importer exposure matrix
- Blocked by: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Blocks: `hormuz-s49.3` - Evaluate China SPR release claims

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.
