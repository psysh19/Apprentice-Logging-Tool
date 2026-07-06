# Apprenticeship Work Activity Log — front-end prototype

A simple Django app for logging work activities against the Data Science
apprenticeship KSBs. This build is **front end only**: there is no database,
no models and no saving. It renders the forms and lets you move between pages.

## What each activity page has

- Student ID (page 1 only)
- Start time and End time (with a live duration hint)
- "This is new learning" tick box
- "Within regular working hours" tick box
- What you did
- What you learned
- KSBs covered — all 27 (K1–K5.3, S1–S8, B1–B6) as tick boxes, grouped into
  Knowledge / Skills / Behaviours. Hover a tick box to see the full descriptor.

There are 10 activity pages by default, navigable via the numbered strip or the
Previous / Next buttons. Only page 1 shows the Student ID field.

## Run it

```bash
pip install django
python manage.py runserver
```

Then open http://127.0.0.1:8000/ — it redirects to the first activity page.

## Change the number of pages

Edit `ACTIVITY_PAGES` at the bottom of `logbook_project/settings.py`.

## Where things live

- `logbook/views.py` — the KSB list (edit labels/descriptions here) and page logic
- `logbook/templates/logbook/activity.html` — the form
- `logbook/templates/logbook/base.html` — layout and all styling (inline CSS)

## Next steps (not built yet)

Wiring up saving would mean adding a model, a form POST handler with CSRF, and a
migration. Happy to add that when you are ready.
