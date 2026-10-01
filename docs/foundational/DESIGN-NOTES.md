# Design Notes

A record of specific decisions made while building this project and
why -- not a tutorial, not a restatement of
[`ARCHITECTURE.md`](ARCHITECTURE.md)'s overview. Each section below is
one decision, kept even after the code around it changes, so a later
reader can tell "we chose X over Y because Z" from "nobody thought of
Y." New entries go at the bottom, oldest first -- this is a log, not
an index.

## Why pywebview, and why the OS title bar stays on

**Decision (Stage 1):** wrap the ARKlight-compiled, Flask-served
output in a [pywebview](https://pywebview.flowrl.com/) native window
(`src/backend/desktop.py`) rather than wait for ARKlight's own native
desktop backend, and keep `frameless=False`.

**Why now, not later:** the reference screenshot's title bar has real
OS window semantics -- minimize, maximize, close, drag. A page in an
ordinary browser tab cannot grant itself control over its own window
for any of these; it's a browser security boundary, not something
more ARKlight markup or CSS could reach around. Without *some* real
window, Stage 1's "convincing static match for the reference
screenshot" done-when criterion can only ever be checked against a
browser tab, which the screenshot it's being checked against isn't.

**Why pywebview specifically, and not wait:** ARKlight's own native
desktop backend (GTK3 + WebKit2GTK) is the architecturally correct
long-term answer -- no second toolkit dependency, no second window
runtime to keep in sync with ARKlight's own output model. It is
confirmed not on `main` yet (checked directly against
`WHAT-ARKLIGHT-IS.md`'s capability table, not assumed from the
pitch). Blocking Stage 1 on an unscheduled upstream feature would have
stalled the whole addendum indefinitely for a problem pywebview
solves today with one extra dependency.

**Why `frameless=False` instead of a borderless window:** the shell's
own drawn title bar (Stage 1's static minimize/maximize/close row)
has no behavior wired to it yet -- clicking those buttons does
nothing. Going frameless now would remove the OS's working controls
and replace them with non-working cosmetic ones, trading "two title
bars stacked on top of each other" for "zero working window
controls." The double-chrome look is the honest cost of being
mid-stage; it flips to `frameless=True` in the same change that wires
the drawn buttons to `window.minimize()` / a maximize toggle /
`destroy()` through pywebview's JS API -- not before.

**Status:** interim. Stage 5 of
[`CLASSIC-SHELL-ADDENDUM.md`](../implementation/CLASSIC-SHELL-ADDENDUM.md)
is where this either gets retired in favor of ARKlight's native
backend, or formally kept -- a call this note deliberately doesn't
pre-make.

## Why Escape-to-close is deferred, not faked

**Decision (Stage 2):** ship "click outside closes the File dropdown"
and explicitly defer "press Escape closes it," rather than build
something that only approximates the latter.

**Why:** the addendum's original Stage 2 wording asked for both,
written before a close read of ARKlight's actual vocabulary. Checking
`arklight/api.py` and the authoring docs directly turned up no
keydown/key-press primitive anywhere in ARKlight -- `on_click` is the
only event its closed vocabulary currently reaches. There is no
`on_keydown=`, no global listener mechanism, and no documented escape
hatch for one (ARKlight deliberately has none for arbitrary JS at
all, for reasons unrelated to this specific gap). Building a
real Escape handler isn't possible without either ARKlight growing a
keyboard-event primitive, or reaching for a raw-JS escape hatch that
doesn't exist and wouldn't fit this project's "no hand-written
JavaScript" stance anyway.

**Why not skip it silently instead:** a gap that isn't written down
tends to get rediscovered the hard way, usually while someone's
mid-way through a different stage. Amending the addendum's own Stage
2 section to say "deferred, blocked on X" costs one paragraph and
means the next person (or the next session of this same assistant)
doesn't have to re-derive the same finding.

**What *did* ship instead:** "click outside closes it," which turned
out to be fully reachable with existing vocabulary -- a full-viewport
`Container` with `position: fixed`, gated by the same
`Show(Predicate.truthy("file_menu_open"), ...)` as the dropdown
itself, with `on_click=Action.set("file_menu_open", False)`. The only
trick needed was `z-index`: the backdrop sits at `10`, the menu bar at
`20`, so a click back on "File" itself still reaches the menu bar's
own `on_click` instead of the backdrop underneath it. No JavaScript
written by hand, no escape hatch -- just existing `style={...}`
properties arranged correctly.

**Status:** tracked gap. Revisit if/when ARKlight ships a keydown
primitive; not blocking any currently-planned stage, since nothing
else in the addendum needs keyboard events.

## Why every File-menu item closes the dropdown, with nothing else wired

**Decision (Stage 2):** each of the eighteen File-menu dropdown rows
gets `on_click=Action.set("file_menu_open", False)` and nothing more
-- except Recent Files, which gets no `on_click` at all.

**Why not a "not wired yet" acknowledgement instead:** the addendum
allowed either a plain no-op or a placeholder acknowledgement.
`on_click` in ARKlight's current vocabulary takes exactly one
`Action.*(...)` per node -- there's no chaining mechanism to both
close the menu and separately set some "last clicked" state for an
acknowledgement message to read. Picking one: closing the menu is the
behavior every real menu item has regardless of whether its actual
action works yet, so it was the one that made the shell feel least
broken while Stage 4 is still pending, rather than the one that drew
more attention to what doesn't work yet.

**Why Recent Files is the one exception:** it's rendered as a
submenu affordance (a `\u25b8` disclosure glyph where every other row
has a shortcut hint), and building a real nested submenu is out of
scope for this stage. Giving it the same "closes the parent menu"
click behavior as a real action item would make it look more
functional than it is -- a submenu that doesn't open shouldn't
close its parent on click either, since that's not what a submenu
affordance does in the reference app. Leaving it with no `on_click`
at all keeps it honestly inert, consistent with how the other twelve
top-level menu labels are handled in both Stage 1 and Stage 2.

**Status:** settled for this stage. Stage 4 replaces the real actions
(New, Open, Save, Save As, Exit) with actual Flask-backed behavior;
everything else on this list stays exactly this inert until its own
future addendum, per the addendum's own "Deliberately out of scope"
section.

## Why Ln/Col/Pos stay hard-coded in Stage 3

**Decision (Stage 3):** ship live `length` and `lines` in the status
bar; leave Ln, Col, Pos (and selection length) hard-coded and amend the
addendum, rather than approximate them.

**Why:** the addendum's Stage 3 wording grouped "line/column position,
selection length" with the fields computable client-side. Reading
ARKlight's vocabulary shows the split is different. `Textarea` takes
`bind_value=Bind.model(...)`, so the document's *text* is state, and
anything that is a function of the text -- character count
(`Derive.string_length`), line count (`Derive.split_count` on `"\n"`)
-- is a `Computed`. But the caret and selection offsets are DOM
properties no primitive reads, and there is no focus/select/keyup
event to trigger a read, so no `Computed` can see them (the same
absence of an event surface that deferred Escape in Stage 2).

**Why not approximate:** the tempting shortcut is to treat the caret as
sitting at the end of the text, deriving Ln/Col/Pos from the last line.
That is right while typing at the end and wrong as soon as the user
clicks or arrows elsewhere -- a status bar that is usually right is
worse than one that is plainly static, because nobody can tell which
state it is in. Same principle as Escape-to-close: do the part that is
real, write down the part that isn't.

**Status:** tracked gap, blocked on ARKlight growing a caret/selection
primitive. Not blocking Stage 4.

## Why closing the only tab shows a notice instead of resetting

**Decision (Stage 3):** the tab's close (x) opens a small dismissible
"isn't wired up yet" notice. It does not close the tab, and does not
reset the editor.

**Why:** the addendum allowed "a no-op or a placeholder prompt." A
real Notepad++ closing its last tab leaves a fresh empty `new 1`, so
resetting `editor_text` looks like the faithful behavior -- but there is
no document lifecycle yet, so it would silently discard whatever was
typed, with none of the save prompt Notepad++ shows. A pure no-op was
the other option and was passed over because a close button that
visibly does nothing reads as broken; the notice says why. It is the
tab-strip analogue of Stage 2's "File items close the menu and do
nothing else."

**Status:** settled for this stage. Stage 4 replaces it with real close
behavior alongside real documents.

## Why the toolbar and the File menu share one handler

**Decision (Stage 3):** new/open/save toolbar icons call
`file_placeholder_action()`, the same function every File-menu row uses,
instead of each carrying its own `Action.set(...)`.

**Why:** the addendum asks that toolbar and menu "agree with each other
from day one instead of being wired twice later." One function means
Stage 4 changes one place, and a test asserts the toolbar icons carry
exactly the action the menu rows do. Only new/open/save are live: the
other File actions on the toolbar (`save-all`, `close`, `print`) are not
named by the addendum for this stage, and everything else belongs to
menus (Edit, Search, View, ...) that are out of scope, so they stay
inert and keep the default cursor so nothing signals a click that does
nothing.

**Status:** settled for this stage.
