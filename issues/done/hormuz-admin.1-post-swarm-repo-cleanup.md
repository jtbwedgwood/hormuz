---
id: "hormuz-admin.1"
title: "Post-swarm repo cleanup and issue tracker normalization"
type: "task"
status: "done"
priority: "P1"
parent: null
labels:
  - "admin"
  - "cleanup"
  - "issue-tracker"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T21:00:00Z"
updated_at: "2026-07-06T21:00:00Z"
---

# Post-swarm repo cleanup and issue tracker normalization

## Description

Take stock of the agent swarm output, normalize tracker state, clean obvious generated cruft, and prepare a consolidated commit.

## Acceptance Criteria

Issue files use documented status folders; deferred or blocked work is explicitly labeled; generated Python cache files are removed from project source directories; final commit includes all research outputs and cleanup changes.

## Dependency Notes

- Standalone admin cleanup requested after the initial research swarm.

## Work Notes

- 2026-07-06: Converted the paid/raw AIS reconstruction child `hormuz-2y7.8` from the undocumented `issues/frozen/` state to the documented `issues/deferred/` state. The cost/scope rationale and blocker remain intact.
- 2026-07-06: Moved unfinished RQ4 stockpile work from `issues/in-progress/` to `issues/blocked/` because remaining closure depends on importer-adjustment tasks and a consolidated buffer table.
- 2026-07-06: Removed stale RQ5 blockers where completed issues already documented stockpile buffering as a caveat rather than a closure blocker.
- 2026-07-06: Removed ignored `__pycache__` directories from `code/` and `scripts/` so the repo scan is cleaner. `.venv/` was left untouched and remains ignored.
- 2026-07-06: Updated root `README.md`, pinned `pytest==8.4.2`, and expanded `data/manifest.csv` so committed derived tables, figure files, and the blog widget have registry rows.
- 2026-07-06: Subagent audit split: issue tracker consistency, research/output inventory, and git/project hygiene.
