# Architecture

_Current as of Stage 3 of
[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](../implementation/CLASSIC-SHELL-ADDENDUM.md)
(the only implementation ladder accepted so far). This file is
updated in place as more of the addendum ships -- cross-check
[`PROGRESS.md`](../../PROGRESS.md)'s Snapshot table before treating
anything stage-specific here as still accurate._

## Vision

The pitch -- a native-feeling Notepad++ experience for Linux, built
as a local web app -- lives in exactly one place: the root
[`README.md`](../../README.md). Kept there, not copied here, for the
same reason ARKlight keeps its own pitch in its root `README.md`
rather than in its `ARCHITECTURE.md`: it's landing-page copy first,
an architecture fact second.

## The three pieces

```
  src/frontend/  (ARKlight)        src/backend/  (Flask + pywebview)
  ----------------------------     -----------------------------------
  Python source (Site, Page,       app.py:    serves ARK/ as static
  components) -- compiles to              files, nothing else yet
  plain HTML/CSS/JS via            desktop.py: opens that served page
  `arklight build site.py`                 in a real native OS window
         |                                      |
         v                                      v
       ARK/   ----------------- served by -----------------> a real
  (build output,                                              window
   gitignored)
```

- **`src/frontend/`** owns everything that can be expressed as
  compiled static output: the window chrome, its styling, and
  whatever client-side interactivity ARKlight's closed
  `State`/`Action`/`Show`/`Predicate` vocabulary can reach (see
  "What ARKlight actually owns" below). Nothing here reads or writes
  a real file, or needs a live process.
- **`src/backend/`** owns everything that needs a real, running
  process. Right now that's narrower than its eventual job: just
  serving `src/frontend/`'s build output as static files
  (`app.py`), plus wrapping that in a real native window
  (`desktop.py`, see "The pywebview amendment" below). File I/O
  (New/Open/Save/Save As/Exit) is Stage 4's job, not built yet.
- **[`notepad-plus-plus-reference/`](../../notepad-plus-plus-reference/)**
  isn't a piece of this app at all -- vendored, read-only, upstream
  Notepad++ source kept around purely as a behavior/visual reference
  (the screenshot this whole addendum is matching came from running
  code in here). Nothing in `src/` imports from it or builds it.

## Why frontend-first, backend-last (per addendum, not a general rule)

This ordering is [`CLASSIC-SHELL-ADDENDUM.md`](../implementation/CLASSIC-SHELL-ADDENDUM.md)'s
own sequencing choice, not a standing architectural principle --
future addenda for other segments (Edit, Search, the real editing
engine) will pick whatever order fits that segment. For *this*
segment, "classic look" is a visual/structural claim that ARKlight
alone can fully settle, so getting it pixel-checked happens before
Flask needs to exist at all. See the addendum's own "Why frontend
first, backend last" section for the full reasoning.

## What ARKlight actually owns, concretely

Confirmed against ARKlight's own docs before any of this was built --
not assumed:

- The full HTML element vocabulary as typed components (`Container`,
  `Span`, `Table`, `Textarea`, ...) -- nothing in the shell needed a
  tag ARKlight doesn't expose.
- Arbitrary CSS via `style={...}` / `site.style(name, rules)`, both
  `{css-property: value}` dicts -- full box-model control (borders,
  shadows, `z-index`, `position`), including a `:pseudo:property`
  shorthand for `:hover`/`:focus`/`:active`/etc. inside the same
  dict. No raw CSS string, no `@media` (ARKlight does intrinsic,
  container-width-based responsive layout instead -- irrelevant here,
  since this app is a fixed-shape window, not a responsive page).
- `State(name, initial)` (page-scoped reactive state, declared as a
  direct child of `Page(...)`), `Action.toggle_bool`/`Action.set`/etc.
  (a closed vocabulary for `on_click`, one action per click, no
  chaining), `Show(Predicate.*, ...)` (conditional rendering). This
  is what Stage 2's File dropdown runs on, entirely. Stage 3 adds
  `bind_value=Bind.model(...)` (two-way textarea binding) and
  `Computed(...)`/`Derive.*` (values derived from state, e.g. the
  status bar's length and line count).
- **What its closed vocabulary doesn't have (yet):** any
  keydown/key-press primitive, and any way to read the caret or
  selection (so no live Ln/Col/Pos --
  see [`DESIGN-NOTES.md`](DESIGN-NOTES.md#why-lncolpos-stay-hard-coded-in-stage-3)).
  `on_click` and input-value binding are the only events ARKlight's
  closed vocabulary reaches right now -- see
  [`DESIGN-NOTES.md`](DESIGN-NOTES.md#why-escape-to-close-is-deferred-not-faked)
  for what that blocked in Stage 2. Both are reachable through
  ARKlight's documented script-extension hatch, which this project has
  chosen not to use (see
  [`DESIGN-NOTES.md`](DESIGN-NOTES.md#correction-arklight-does-have-an-escape-hatch)).
  The vocabulary also has no children-slot for
  user-defined components (content goes through declared props
  instead) -- relevant if a `Menu`/`MenuItem` component ever gets
  factored out of `components/shell.py`'s current plain-function
  style.

## The pywebview amendment

A browser tab cannot grant a page control over its own window's
minimize/maximize/close/drag -- a security boundary, not an ARKlight
gap. ARKlight's own native desktop backend (GTK3 + WebKit2GTK) is the
correct long-term fix and isn't on `main` yet. `src/backend/desktop.py`
is the interim stand-in: [pywebview](https://pywebview.flowrl.com/)
opens `app.py`'s Flask-served build in a real native OS window. Full
reasoning, including why the OS's own title bar stays on for now
(`frameless=False`), is in
[`DESIGN-NOTES.md`](DESIGN-NOTES.md#why-pywebview-and-why-the-os-title-bar-stays-on).
This is explicitly an interim delivery mechanism, not a permanent
architectural commitment -- Stage 5 either retires it in favor of
ARKlight's own native backend, or formally keeps it, whichever makes
sense once that backend actually exists.

## Source of truth for hard-coded content

Every value the shell currently renders that isn't yet backed by real
state or a real file -- menu labels, toolbar icon groups, File-menu
items and their shortcut hints, status bar defaults -- lives in one
place, `src/frontend/content/site_content.py`, not scattered across
component code. This is so each later stage (3 replacing status-bar
hard-codes with computed values, 4 wiring File items to real actions)
has exactly one file to check for what it's replacing. (Stage 3 did
that for length/lines: those `STATUS_SEGMENTS` entries are now dicts
naming a `Computed` instead of strings.)

## Testing strategy

`src/frontend/tests/test_site.py` is a build-smoke suite, not a
pixel-diff: it builds the real site into a temp directory and asserts
on the compiled HTML's structure -- region order, label order,
presence or absence of `data-ark-*` attributes on specific elements.
It catches a reordered region, a menu item that gained or lost
`on_click` it shouldn't have, or a broken import; it does not catch a
color or spacing regression. Visual fidelity against the reference
screenshot is checked by hand (see `PROGRESS.md`'s Stage 1/2 detail
entries for what was actually spot-checked and how, given this
project has no headless-browser screenshot tooling set up yet).

## Deliberately not architecture yet

- Real multi-document/multi-tab behavior, a document model.
- The Scintilla-equivalent editing engine: syntax highlighting, line
  folding, anything beyond a plain `Textarea`.
- Any menu-bar item other than File.
- A settled answer on whether `pywebview` survives past Stage 5.

Each becomes a real architecture fact here once it's actually built,
the same way the pywebview amendment just did -- not before.
