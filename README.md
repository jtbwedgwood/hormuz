# Hormuz

Research workspace for a rigorous blog post on the Strait of Hormuz shock.

Start with:

- `AGENTS.md` for project rules, issue workflow, and Python environment rules.
- `issues/` for task state, working notes, source breadcrumbs, blockers, and handoffs.
- `docs/README.md` for reusable user-facing research outputs.
- `data/manifest.csv` for source and output registry.

Use the repository-local Python environment:

```bash
.venv/bin/python -m pytest -q
```

Committed outputs live in `data/derived/`, `figures/`, `docs/`, and approved blog artifacts in `blogpost/`. Raw/private/cache data should stay out of git unless explicitly curated.
