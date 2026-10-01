# Classic Shell Addendum: Staged Order

**Status:** Accepted. Stage 1, 2 and 3 of 5 SHIPPED. This is the first
segment of the larger "divide the app into segments, ship one at a
time" plan -- everything else on that list (Edit menu, Search menu,
the actual editing engine, tabs-with-real-documents, and so on) is
out of scope here and waits for its own addendum once this one ships.

We are not trying to rebuild Notepad++ end to end in one pass. We are
taking the single most load-bearing piece of "does this look and feel
like Notepad++" -- the classic shell you see the instant the app
opens, with the File menu sitting exactly where a Notepad++ user
expects it, above and before everything else -- and shipping *that*,
completely, before touching anything downstream of it. Everything
after this addendum assumes the shell from this one already exists.

## Why the File menu specifically, and why first

Open a copy of Notepad++ and the File menu is the first thing your
eye and your muscle memory land on: top-left, first in the menu bar,
and the busiest menu in the app (New, Open, Save, Save As, Recent
Files, Exit -- the operations that exist before you've typed a single
character). If the shell doesn't get File right, nothing else about
"classic look" reads as credible, no matter how faithful the rest of
the chrome is. So File is the one menu this addendum takes all the
way to working, end to end; every other menu in the bar (Edit,
Search, View, Encoding, Language, Settings, Tools, Macro, Run,
Plugins, Window, `?`) is rendered -- present, correctly labeled, in
the correct order -- but deliberately inert until its own future
addendum.

## Why frontend first, backend last

The "classic look" is, by definition, a visual and structural claim:
title bar, menu bar, toolbar row, tab strip, status bar, all in the
right place, all styled right, before a single byte gets read from or
written to disk. ARKlight compiles that whole claim to static HTML/
CSS with zero backend involvement, so we can get it pixel-checked and
signed off long before Flask needs to exist at all. Wiring File's
actual menu items to real file I/O is the *last* rung, not because
it's unimportant, but because it's the one part of this addendum that
can't be verified by looking at the screen -- everything upstream of
it can.

## A delivery-mechanism amendment: pywebview, ahead of schedule

One piece of "look and feel like Notepad++" can't be settled by
ARKlight output alone, no matter how pixel-faithful it is: the title
bar's minimize/maximize/close/drag are real OS window actions in the
reference screenshot, and a page sitting in an ordinary browser tab
has no way to grant itself control over its own window for any of
them -- that's a browser security boundary, not an ARKlight gap.
ARKlight's own native desktop backend (GTK3 + WebKit2GTK) is the
eventual, correct answer to that, and isn't on `main` yet.

Rather than let Stage 1 sit un-openable-as-a-real-window until that
backend ships, `src/backend/` now carries a minimal Flask app
(`app.py`) that serves the `arklight build` output as static files,
and `desktop.py`, which opens that same served page inside a real,
native OS window via [pywebview](https://pywebview.flowrl.com/)
instead of a browser tab. This is *not* Stage 4 or Stage 5 -- no
File-menu endpoint exists yet, and the OS's own title bar stays on
(`frameless=False`) precisely because Stage 1's drawn
minimize/maximize/close row is still cosmetic, so going frameless now
would trade "two title bars" for "zero working ones." It's narrowly
the "serve the build as one app" half of Stage 5, pulled forward
because it was the only way to get a real window to pixel-check Stage
1 against in the first place. Stage 5, when its turn comes, is what
replaces `pywebview` with ARKlight's own native backend (or formally
keeps `pywebview`, if that native backend still isn't ready) and wires
Stage 4's real File-menu routes into the drawn menu's `on_click`
targets -- this amendment only covers getting pixels on screen in a
real window, nothing more.

## Stage 1 of 5 -- Static shell, no interactivity (frontend only) -- SHIPPED

Pure ARKlight output: a `Page` that renders the whole window chrome as
plain markup, with every value the classic look depends on hard-coded
for now (no `State`, no `on_click`, nothing dynamic).

- Title bar: window icon placeholder, title text
  (`<filename> - Notepad++`-style, filename hard-coded), the
  minimize/maximize/close button row as static icons only.
- Menu bar: all thirteen top-level labels, left-aligned, File first,
  in the exact order shown in the reference screenshot (File, Edit,
  Search, View, Encoding, Language, Settings, Tools, Macro, Run,
  Plugins, Window, `?`). None of them open anything yet -- this stage
  proves placement and typography, not behavior.
- Toolbar row: the classic icon strip beneath the menu bar, rendered
  as static icons in the reference layout. No click targets.
- Editor area: an empty, classic-styled text pane with line-number
  gutter, taking up the body of the window.
- Status bar: the bottom strip (`Normal text file`, line/column
  position, line ending style, encoding), values hard-coded to
  plausible defaults.
- **Done when:** a compiled `arklight build` output, opened in a
  browser, is a convincing static match for the reference screenshot
  -- same regions, same order, same proportions. No `arklight.js`
  runtime is even expected to ship yet, since nothing on the page is
  stateful.
- **Where it lives:** `src/frontend/components/shell.py` (markup +
  `register_styles`), `src/frontend/content/site_content.py`
  (every hard-coded value above, named and commented so Stage 2/3
  know exactly what they're replacing), `src/frontend/pages/home.py`,
  `src/frontend/site.py`. `src/frontend/tests/test_site.py` checks
  the eight regions render in the reference screenshot's order and
  all thirteen menu labels are present and correctly ordered -- not a
  pixel-diff, but enough to fail loudly if a future edit reorders or
  drops a region. No `arklight.js` in the build output, as expected.

## Stage 2 of 5 -- File menu opens and closes (frontend only) -- SHIPPED

The one menu this addendum is actually about, made interactive. Still
zero backend -- this stage is ARKlight's `State`/`Bind`/`Action`
vocabulary and nothing else.

- `State("file_menu_open", False)` gates the File dropdown's
  visibility; clicking "File" in the menu bar toggles it
  (`Action.toggle_bool`), clicking anywhere outside it closes it.
- The dropdown itself, populated with Notepad++'s classic File-menu
  items in their classic order (New, New Window, Open..., Open
  Folder..., Open in Explorer, Reload, Save, Save As..., Save a
  Copy As..., Save All, Rename, Close, Close All, Close All but
  Current, Recent Files submenu, Print, Print Now, Exit), each with
  its classic keyboard-shortcut hint rendered to the right of the
  label the way Notepad++ shows it -- but every item is a no-op click
  target for now (or, at most, fires a placeholder "not wired yet"
  visual acknowledgement rather than any real file action).
- The other twelve menu-bar labels stay exactly as inert as they were
  in Stage 1 -- this stage does not give them dropdowns.
- **Done when:** clicking "File" opens a dropdown that looks and
  orders itself like the reference, closes correctly, and every other
  menu remains visibly, deliberately unclickable.
- **Amendment -- "pressing Escape closes it" is deferred, not built:**
  the line above was this stage's original ask, written before a
  closer read of ARKlight's vocabulary. There is currently no
  keydown/key-press primitive in ARKlight at all -- `Action.*` fires
  only from `on_click`, and there's no `on_keydown`/global listener
  mechanism to hang an Escape handler off of. "Click outside closes
  it" *is* fully buildable without one (a full-viewport backdrop,
  `Show`-gated by the same `file_menu_open` state, stacked under the
  menu bar via plain `z-index` so a click back on "File" still reaches
  File's own handler) and is what actually shipped. Escape-to-close
  waits for ARKlight to grow a keyboard-event primitive -- tracked as
  a gap, not silently dropped or faked with something that only looks
  like it works.
- **Where it lives:** `components/shell.py`'s `file_dropdown()` and
  the rewritten `menu_bar()`; `content/site_content.py`'s
  `FILE_MENU_ITEMS` (labels, order, grouping, shortcut hints --
  `New`/`Open`/`Save`/`Save As`/`Close`/`Print`/`Exit` are the
  commonly-known defaults, not checked against a live Notepad++
  install; left blank elsewhere rather than guessed); `pages/home.py`
  declares `State("file_menu_open", False)` on the `Page`. Four new
  tests in `tests/test_site.py` cover: File has real `on_click`
  wiring and the other twelve don't; dropdown items render in classic
  order; Recent Files has no click behavior (no real submenu this
  stage); the backdrop closes the menu via the same state key.

## Stage 3 of 5 -- Toolbar, tabs, and status bar come alive (frontend only) -- SHIPPED

Rounds out the shell's remaining interactive-but-backend-free
surface, so that by the end of this stage the only thing not working
is the thing that genuinely needs a backend: actual file I/O.

- Toolbar icons get hover/pressed states; the icons that map to
  File-menu actions (new, open, save) become clickable and route to
  the same (still-placeholder) handlers Stage 2 gave those menu
  items, so the toolbar and the menu agree with each other from day
  one instead of being wired twice later.
- Tab strip: a single hard-coded "new 1" tab, styled as the active
  tab, with a working close (`x`) affordance -- closing the only tab
  is allowed to be a no-op or show a placeholder prompt, since there's
  no real document lifecycle yet.
- Status bar fields that can genuinely be computed client-side without
  a backend (line/column position, selection length) start reflecting
  the (still-empty) editor pane for real; fields that require a real
  file (encoding, line-ending style, "Normal text file" vs. something
  else) stay hard-coded until Stage 4/5.
- **Done when:** every piece of chrome in the reference screenshot
  that *can* be genuinely interactive without a backend, is.
- **Amendment -- caret-dependent status fields are deferred, not
  faked:** the status-bar bullet above named "line/column position,
  selection length" as client-side computable. A closer read of
  ARKlight's vocabulary says otherwise: `Textarea` can be two-way
  bound to `State` (`bind_value=Bind.model(...)`), which is enough
  to derive *document* length and line count, but nothing exposes the
  caret or selection offsets (`selectionStart`/`selectionEnd`), and
  there is no focus/select/keyup event to hang a handler off of --
  the same missing-event-surface that deferred Escape in Stage 2.
  Ln, Col, Pos and selection length therefore stay hard-coded (`Ln :
  1`, `Col : 1`, `Pos : 1`) rather than being approximated -- e.g.
  assuming the caret sits at the end of the text would be right while
  typing and wrong the moment someone clicks elsewhere. Tracked as a
  gap blocked on ARKlight growing a caret/selection primitive.
  `length` and `lines` *did* ship live.
- **What shipped:**
  - Toolbar: new, open and save are clickable and fire the same
    placeholder handler as their File-menu rows (one shared
    function, `file_placeholder_action()`, so Stage 4 swaps it in one
    place). Every toolbar icon gets a pressed (`:active`) state on top
    of Stage 1's hover; only the three live icons get a pointer
    cursor. The other eleven stay inert (Edit/Search/View/... are
    out of scope; `save-all`, `close` and `print` are File actions
    but the stage only names new/open/save).
  - Tab strip: the single "new 1" tab's close (x) opens a small
    dismissible notice ("Closing the last tab isn't wired up yet")
    rather than doing anything. Silently resetting the editor would
    have discarded typed text with none of Notepad++'s save prompt,
    so the placeholder-prompt option was taken over the no-op one.
  - Editor + status bar: the textarea is bound to
    `State("editor_text")`; `length` and `lines` are
    `Computed(...)` values (`Derive.string_length`,
    `Derive.split_count`) rendered through `Bind(...)`. Encoding, EOL
    style and "Normal text file" stay hard-coded until Stage 4/5.
- **Where it lives:** `components/shell.py` (`file_placeholder_action`,
  `_toolbar_icon`, `tab_strip`, `status_bar`), `content/site_content.py`
  (`TOOLBAR_FILE_ACTIONS`, `CLOSE_TAB_NOTICE`, the dict-shaped live
  entries in `STATUS_SEGMENTS`), `pages/home.py` (the two new
  `State`s and two `Computed`s). Five new tests in
  `tests/test_site.py`; the page was additionally exercised in jsdom
  (typing, tab close, toolbar vs. menu) -- not committed, see
  `PROGRESS.md`.

## Stage 4 of 5 -- Flask comes in, File-menu endpoints only (backend)

The first backend code this addendum touches. Scope is deliberately
narrow: exactly the File-menu operations that need a real process
(disk access), nothing that belongs to a future addendum.

- Minimal Flask app: routes for `New`, `Open` (native-feeling file
  picker, or the closest equivalent a local web app can offer),
  `Save`, `Save As`, and `Exit`. Recent Files, Open Folder, Open in
  Explorer, Reload, Save a Copy As, Save All, Rename, Close variants,
  and Print are left as the still-inert placeholders Stage 2 gave
  them -- they're real File-menu items, but wiring all of them is
  more than this addendum's "get File working end to end" claim
  requires, and pulling every one of them in now would blur this
  stage's scope. (Which of these, if any, get pulled forward into
  this addendum rather than deferred to a later one is a maintainer
  call to make once Stage 4 is actually underway, not a decision this
  doc is pre-committing to.)
- No routing/state design beyond what those five operations need --
  no attempt yet at a general "document model" that later segments
  (Edit, Search, real multi-tab editing) will eventually require.
- **Done when:** New/Open/Save/Save As/Exit each do the real thing,
  backed by Flask, with no visual change to the shell Stages 1-3
  already delivered.

## Stage 5 of 5 -- Serve it as one app (backend)

Glue, not design. Everything upstream of this stage already works in
isolation (ARKlight build output in a browser; Flask routes testable
on their own); this stage is what makes opening the app mean
"classic-looking Notepad++ shell, with a working File menu,
served from one place."

- `arklight build` output wired as the static asset Flask serves --
  **already in place**, ahead of schedule, as `src/backend/app.py`;
  see "A delivery-mechanism amendment" above for why. What's still
  actually Stage 5's own work: swapping `pywebview` for ARKlight's
  native backend once it exists (or formally keeping `pywebview`, a
  maintainer call to make when that backend actually ships, not now),
  and flipping `desktop.py`'s window to `frameless=True` once the
  drawn title bar's buttons are real.
- Flask's File-menu routes reachable from the compiled frontend's
  `on_click` targets in place of Stage 2-4's placeholders.
- **Done when:** running the app end to end -- one command, one
  process -- opens to the reference look, and File > New/Open/Save/
  Save As/Exit all genuinely work.

## Deliberately out of scope for this addendum

- Every menu-bar item other than File (Edit, Search, View, Encoding,
  Language, Settings, Tools, Macro, Run, Plugins, Window, `?`) --
  each is its own future segment, same one-at-a-time approach.
- Real multi-document / multi-tab behavior -- Stage 3's tab strip is
  cosmetic, not a document manager.
- Syntax highlighting, the Scintilla-equivalent editing engine, dark
  mode, and anything else in
  [`notepad-plus-plus-reference/`](../../notepad-plus-plus-reference/)
  that isn't part of the shell itself.

## Graduation

Once all five stages ship, whatever in here is a permanent design
decision (the ARKlight-frontend/Flask-backend split for a shell
segment, in particular) graduates into
[`docs/foundational/`](../foundational/README.md) the same way any
other completed implementation ladder does; this file is then trimmed
or removed per [`docs/implementation/README.md`](README.md)'s own
rule.
