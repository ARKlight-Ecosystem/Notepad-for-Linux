# Frontend

This is where the [ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight)
source lives -- the `Site`/`Page`/component Python that compiles down
to the plain, dependency-free HTML/CSS/JS the app actually ships.
Nothing here is hand-written JavaScript; if a piece of UI needs
client-side behavior, it's expressed through ARKlight's
`State`/`Bind`/`Action` vocabulary, not a `<script>` tag.

## Status

Empty. The first thing to land here is Stage 1 of
[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](../../docs/implementation/CLASSIC-SHELL-ADDENDUM.md)
-- the static classic shell (title bar, menu bar, toolbar row, tab
strip, editor pane, status bar), every value hard-coded, no `State`
yet. Stages 2 and 3 of that same addendum build directly on top of
what Stage 1 puts here; Stages 4 and 5 are backend work and belong in
[`src/backend/`](../backend/README.md) instead.

## What belongs here

- ARKlight `Page`/component source for the app's UI.
- Nothing that reads or writes a real file, touches the filesystem, or
  needs a live process running -- that's `src/backend/`'s job, wired
  in through `on_click` targets once Stage 4 of the addendum exists.

## Layout

No files yet, so no layout to describe. Whether this ends up as a
single `Site` with one `Page` per view, a `components/` folder for
shared chrome, or something else is a call to make once Stage 1
actually starts -- not something this README is pre-deciding.
