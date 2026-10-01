# Changelog

All notable changes to this project are tracked here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/). This project
doesn't version itself (no releases, no tags yet) the way ARKlight
does -- entries are grouped by addendum stage instead, same unit of
work [`docs/implementation/`](docs/implementation/README.md) tracks.
For the narrative version of the same history -- what was tried,
what was rejected, why -- see [`PROGRESS.md`](PROGRESS.md).

## [Unreleased]

Docs pass: added this file, `PROGRESS.md`,
[`docs/foundational/ARCHITECTURE.md`](docs/foundational/ARCHITECTURE.md),
and
[`docs/foundational/DESIGN-NOTES.md`](docs/foundational/DESIGN-NOTES.md).
No code change.

## Stage 3 -- Toolbar, tabs and status bar come alive

[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](docs/implementation/CLASSIC-SHELL-ADDENDUM.md),
Stage 3 of 5.

- Toolbar: new/open/save icons are clickable and fire the same
  placeholder handler as their File-menu rows
  (`file_placeholder_action()`); every icon gains a pressed state; the
  other eleven icons stay inert.
- Tab strip: the only tab's close (x) opens a dismissible
  placeholder notice instead of doing anything destructive.
- Editor/status bar: the textarea is two-way bound to
  `State("editor_text")`; `length` and `lines` are live
  (`Computed` via `Derive.string_length` / `Derive.split_count`).
- Not built: live Ln/Col/Pos and selection length -- ARKlight has no
  caret/selection primitive. They stay hard-coded; the addendum is
  amended and the gap tracked, not faked.
- `tests/test_site.py`: five new tests (toolbar/menu agreement, the
  other icons staying inert, tab close notice, editor binding + live
  fields, caret/file-dependent fields staying hard-coded). 13/13 pass.

## Stage 2 -- File menu opens and closes

[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](docs/implementation/CLASSIC-SHELL-ADDENDUM.md),
Stage 2 of 5.

- File's menu-bar item is interactive: `State("file_menu_open")`,
  `Action.toggle_bool` on click, a `Show`-gated dropdown with all
  eighteen classic File-menu rows in order (separators, keyboard-
  shortcut hints), and a full-viewport backdrop that closes the menu
  on an outside click without swallowing a click back on "File"
  itself. The other twelve menu-bar labels are untouched -- still
  plain, inert labels.
- Recent Files renders the classic disclosure glyph but gets no
  `on_click` -- a real nested submenu is out of scope for this stage.
- Amended the addendum: "pressing Escape closes it" was the stage's
  original wording, written before confirming ARKlight has no
  keydown/key-press primitive at all. Deferred and tracked as a gap
  rather than faked. "Click outside closes it" is the part that's
  real, built as a plain `z-index`-stacked backdrop -- no JS escape
  hatch needed.
- `tests/test_site.py`: four new tests (File's `on_click` wiring, the
  other twelve staying inert, dropdown item order, Recent Files
  staying inert, the backdrop closing via the same state key). 8/8
  pass.

## Stage 1 -- Static classic shell

[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](docs/implementation/CLASSIC-SHELL-ADDENDUM.md),
Stage 1 of 5.

- `src/frontend/components/shell.py`: the whole window chrome as
  static ARKlight output -- title bar, menu bar (all thirteen
  labels, File first), toolbar icon strip, tab strip, editor pane
  with line-number gutter, status bar. Hard-coded values live in
  `src/frontend/content/site_content.py`. No `State`, no `on_click`
  yet.
- Dropped the generic `arklight new` scaffold's nav bar, footer, and
  About page -- a single-window desktop app doesn't have those.
- `tests/test_site.py`: the eight shell regions render in the
  reference screenshot's order; all thirteen menu labels are present
  and correctly ordered.
- **Delivery-mechanism amendment, pulled forward from Stage 5:** a
  page in an ordinary browser tab can't grant itself control over its
  own window's minimize/maximize/close/drag, and ARKlight's own
  native desktop backend isn't on `main` yet. `src/backend/app.py`
  (Flask, serves the `arklight build` output) and
  `src/backend/desktop.py` ([pywebview](https://pywebview.flowrl.com/),
  opens that served page in a real native OS window) exist to get a
  real window to pixel-check Stage 1 against. Not Stage 4/5 itself --
  no File-menu endpoint exists -- and the OS's own title bar stays on
  (`frameless=False`) since the drawn title bar's buttons are still
  cosmetic. See
  [`docs/foundational/DESIGN-NOTES.md`](docs/foundational/DESIGN-NOTES.md)
  for the full reasoning.

## Scaffolding

- `arklight new` project template initialized in `src/frontend/`.
- Documentation lifecycle (`docs/proposal/`, `docs/implementation/`,
  `docs/foundational/`) established, mirroring
  [ARKlight's own](https://github.com/ARKlight-Ecosystem/ARKlight/blob/main/docs/README.md).
