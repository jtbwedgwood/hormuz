---
id: "hormuz-ccx.11"
title: "Simplify supplier-side oil figure"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-ccx"
labels:
  - "figures"
  - "supply"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "codex"
created_at: "2026-07-14T23:10:00Z"
updated_at: "2026-07-14T23:20:00Z"
---

# Simplify supplier-side oil figure

## Description

Limit the supplier-side figure to Saudi Arabia, UAE, and Iraq; remove the commodity section label; revise the title and number formatting; and restore white percentages on recoverable bars.

## Acceptance Criteria

- Figure and companion CSV contain only Saudi Arabia, UAE, and Iraq oil rows.
- Figure has no oil section label and uses the requested question title.
- UAE and Iraq recoverable values display as `0.7` and `0.3`.
- Recoverable bars show legible white percentage labels.
- Existing methodology document is unchanged.

## Work Notes

- 2026-07-14: Claimed for the requested visual simplification. No research or methodology changes are required.
- 2026-07-14: Updated the builder, companion CSV, and SVG to contain only Saudi Arabia, UAE, and Iraq. Removed the oil section label, changed the title, formatted the two smaller values as `0.7` and `0.3`, and added white `59%`, `21%`, and `8%` labels to the recoverable bars. The methodology document was not edited.
- 2026-07-14: Validation passed: generated with the repository virtual environment, checked exact row/value/title/percentage content, passed `xmllint` and `git diff --check`, and visually inspected a 1440x500 Chrome render for clipping, overlap, and label contrast.
