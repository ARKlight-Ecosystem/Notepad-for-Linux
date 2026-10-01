# Notepad++ for Linux -- Progress

Living document tracking what's implemented, key decisions made along
the way, and what's queued up next. Detail sections below are kept in
reverse-chronological order (newest first) -- the narrative record of
what was tried, what was decided, and why. For the plain, dated list
of shipped changes, see [`CHANGELOG.md`](CHANGELOG.md); for the
settled architecture these decisions landed in, see
[`docs/foundational/ARCHITECTURE.md`](docs/foundational/ARCHITECTURE.md)
and
[`docs/foundational/DESIGN-NOTES.md`](docs/foundational/DESIGN-NOTES.md).

## Snapshot

Status of each rung on the one implementation ladder accepted so far
-- [`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](docs/implementation/CLASSIC-SHELL-ADDENDUM.md).

| Stage | Covers | Status |
| --- | --- | --- |
| Scaffolding | `arklight new` project template, doc lifecycle | DONE |
| 1 of 5 | Static classic shell (title bar, menu bar, toolbar, tab strip, editor pane, status bar) | DONE |
| -- amendment | Flask + pywebview interim native window, pulled forward from Stage 5 | DONE |
| 2 of 5 | File menu opens/closes, click-outside-closes | DONE |
| -- (deferred) | Escape-key-closes -- no keydown primitive in ARKlight yet | BLOCKED (upstream) |
| 3 of 5 | Toolbar/tabs/status bar come alive (frontend-computable fields) | PLANNED |
| 4 of 5 | Flask File-menu endpoints (New/Open/Save/Save As/Exit) | PLANNED |
| 5 of 5 | Serve it as one app; retire or formalize the pywebview amendment | PLANNED |

## Detail

### Stage 2 -- File menu opens and closes

File's menu-bar item became the one genuinely interactive piece of
the shell: `State("file_menu_open", False)` on the page,
`Action.toggle_bool` on the "File" label, a `Show`-gated dropdown
listing all eighteen classic File-menu rows (New through Exit, correct
grouping and separators), and a full-viewport backdrop that closes the
menu on an outside click. The other twelve menu-bar labels are
untouched.

Two decisions worth recording here rather than just in a commit
message (full write-ups in `docs/foundational/DESIGN-NOTES.md`):

- **Escape-to-close was scoped out, not faked.** The addendum's
  original Stage 2 wording assumed both "click outside" and "press
  Escape" would close the dropdown. A closer read of ARKlight's
  closed vocabulary turned up no keydown/key-press primitive at all
  -- `Action.*` only fires from `on_click`. Rather than reach for
  something that only looks like it works, the addendum itself got
  amended: click-outside shipped, Escape is tracked as a gap blocked
  on ARKlight growing a keyboard-event primitive.
- **Every File-menu item closes the dropdown on click, but does
  nothing else.** The addendum allowed either a plain no-op or a
  placeholder "not wired yet" acknowledgement. `on_click` only
  accepts a single action per node (no chaining in the current
  vocabulary), so "close the menu" and "show an acknowledgement"
  couldn't both ride the same click. Closing was picked -- it's the
  one behavior a real menu item always has, whether or not its actual
  action is wired up yet, and it means the shell doesn't feel broken
  while Stage 4 is still pending.

Verified, not just written: build is clean (`arklight build site.py`,
zero warnings), `arklight.js` now ships (the page is stateful),
compiled HTML/CSS spot-checked directly (`data-ark-on-click`,
`data-ark-show`, the `z-index` stacking), 8/8 tests pass, and
`src/backend/app.py`'s Flask app was re-checked serving the new build
end to end.

### Stage 1 -- Static classic shell, plus the pywebview amendment

The shell itself was the easy half: ARKlight's full HTML element
vocabulary, arbitrary `{css-property: value}` styling via
`site.style()`, and system font stacks were enough to match the
reference screenshot's regions, order, and proportions with zero
gaps -- confirmed by reading `WHAT-ARKLIGHT-IS.md`,
`AUTHORING-GUIDE.md`, and `DESIGN-NOTES.md` from the ARKlight repo
itself before writing a line of this project's own code, not assumed.

The harder half was the title bar. The reference screenshot's
minimize/maximize/close/drag are real OS window actions; a page in a
plain browser tab cannot grant itself control over its own window for
any of them, by design -- that's a browser security boundary, not
something more ARKlight code could work around. ARKlight's own native
desktop backend (GTK3 + WebKit2GTK) is the eventual, correct fix, and
isn't on `main` yet. Rather than leave Stage 1 un-openable as a real
window until that backend ships, `src/backend/app.py` (Flask, static
file server for the `arklight build` output) and `src/backend/desktop.py`
([pywebview](https://pywebview.flowrl.com/), opens that served page in
a real native window) were pulled forward from Stage 5. The window
keeps its OS title bar (`frameless=False`) rather than going borderless,
because the shell's own drawn title-bar buttons are still cosmetic --
going frameless now would have traded "two title bars" for "zero
working ones."

### Scaffolding

`arklight new` produced a working, buildable project template in
`src/frontend/` -- confirmed by actually running `arklight build`
against it before building anything on top. The generic scaffold's
nav bar, footer, and About page were dropped in Stage 1 rather than
kept around, since none of them fit a single-window desktop app.

## Next up

Stage 3 (toolbar/tabs/status bar interactivity) is next in the
addendum's own order. No work has started on it yet.
