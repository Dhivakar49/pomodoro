# FocusAI — Upgraded UI

Drop-in replacement for the `frontend/` folder of your Django project.

## What's inside
- `frontend/templates/` — redesigned base + dashboard, tasks, uploads, analytics
- `frontend/static/css/style.css` — full professional design system (dark, gradient, glass)
- `frontend/static/js/` — your original JS files (unchanged, all element IDs preserved)

## Install
1. Back up your existing `frontend/` folder.
2. Replace it with the `frontend/` folder from this package.
3. Run `python manage.py collectstatic` if you use it, then start the server.

All template block names, element IDs (`#timer`, `#taskSelect`, `#taskList`,
`#documentList`, `#stats`, `#chart`, `#totalSessions`, `#totalMinutes`,
`#tasksCompleted`, etc.) and form field names are kept the same so your
existing backend + JS continue to work without changes.
