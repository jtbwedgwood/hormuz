# Hormuz

The purpose of this project is to try to understand as much as possible about the current situation regarding the Strait of Hormuz.
This is not a codebase, it's a data science project. The ultimate goal is to turn this into a blog post. We want to be RIGOROUS
but also find INTERESTING, eye-catching results. Naturally a lot of these items will not be 100% knowable, let's try to find our best guess. Research questions:
- Can we make a reliable daily Hormuz ship tracker with historical data? This is surprisingly hard to find online. I am thinking like in early covid when they had that chart of number of cases, but number of ships
- What are the major products that are disrupted due to these ships? We all know oil, LNG, fertilizer - anything else important? How much of that supply specifically has been taken off the market as far as we know?
- Where specifically were these exports sent to previously? Of the major importer before the closure, where are they now getting the energy etc that they need (or are they just reducing consumption)?
- To the extent that we know this how much have countries' strategic petroleum reserves or other energy stockpiles helped this? Has China really been releasing a ton of its SPR?
- Can we make a reasonable estimate of how much the increase in oil / other commodity prices will increase how much US businesses have to spend? I'm particularly curious about AI - how much has this raised the "cost per token" for example?
- Can we make a comparison of this to other shocks in history? How does it compare to 2002, the 70s ones, etc (taking into account a wide variety of circumstantial differences, not just being dumb and comparing the amount of oil)?

## Rules

Be rigorous. Cite your sources. Don't make unnecessary docs; put task metadata, working notes, and source breadcrumbs in issue files.
Think of it this way: process in `issues/`, output in docs. Concise, relevant.
Just work on main but don't fuck anyone else's work up. Multiple subagents likely to be working in this repo.
When spawning subagents, don't be super stingy but consider spawning medium/low reasoning or cheaper models if that could get the job done.
- Do not delete the root `.gitignore`. It is required project hygiene; update it when needed instead of removing it.

## Python Environment

Use the repository-local virtual environment at `.venv/` for all Python work in this project.

- Before running Python scripts, notebooks, or package installs, activate it with `source .venv/bin/activate` from the repo root, or call tools explicitly through `.venv/bin/python` and `.venv/bin/pip`.
- Do not install project dependencies into the system Python or another virtual environment unless the user explicitly requests it.
- Record every Python package needed for reproducible project work in `requirements.txt`, with pinned versions when practical.
- When adding, upgrading, or removing a package, update `requirements.txt` in the same change and note why in the relevant issue file's `Work Notes`.
- Do not commit `.venv/`; it is local runtime state. Recreate it with `python3 -m venv .venv` and then install dependencies with `.venv/bin/pip install -r requirements.txt`.

## Markdown Issue Tracker

This project uses local Markdown files in `issues/` for task tracking. Do not use external issue trackers, TodoWrite, TaskCreate, or markdown TODO lists elsewhere in the repo.

### Layout

- `issues/open/epics/` - open epics or research questions.
- `issues/open/tasks/` - open discrete tasks.
- `issues/in-progress/` - claimed work.
- `issues/blocked/` - work that cannot proceed without a stated blocker.
- `issues/done/` - completed work.
- `issues/deferred/` - valid but intentionally postponed work.

### Rules

- Each Markdown file represents one discrete unit of work. Use `type: "epic"` in frontmatter only for broad coordinating work; normal research, data, chart, or writing jobs should be `type: "task"`.
- Keep each issue in the folder matching its current status. To claim work, move its file to `issues/in-progress/` and set `status: "in_progress"`. When done, move it to `issues/done/` and set `status: "done"`.
- Preserve stable issue IDs in frontmatter and filenames when moving files. Use `parent`, `blocked_by`, `blocks`, and `children` fields to keep epic/task relationships explicit.
- Put research notes, source links, assumptions, dead ends, and handoff context in the relevant issue file's `Work Notes` section. Keep docs user-facing.
- When adding a new issue, include frontmatter with at least `id`, `title`, `type`, `status`, `priority`, `parent`, `labels`, `blocked_by`, and `blocks`.
