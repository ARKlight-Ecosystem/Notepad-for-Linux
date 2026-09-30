# Backend

The [Flask](https://flask.palletsprojects.com/) app that serves the
compiled ARKlight output and handles everything a static compiler
can't: reading and writing files on disk, and anything else this
editor needs that requires a real, running process.

## Status

Empty. Nothing lands here until
[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](../../docs/implementation/CLASSIC-SHELL-ADDENDUM.md)
reaches Stage 4 -- the File-menu endpoints (New, Open, Save, Save As,
Exit) -- and Stage 5, which serves the ARKlight build output as this
app's static asset. Stages 1 through 3 of that addendum are
frontend-only and don't touch this folder at all.

## What belongs here

- The Flask app and its routes.
- File-system access and any other operation that genuinely needs a
  live process, scoped to whatever the current addendum stage
  actually asks for -- not a general-purpose API surface built ahead
  of need.

## What doesn't

- Anything ARKlight can already express as compiled static output --
  that's [`src/frontend/`](../frontend/README.md)'s job.

## Layout

No files yet -- routing and app structure are a Stage 4 decision, not
one this README is pre-deciding.
