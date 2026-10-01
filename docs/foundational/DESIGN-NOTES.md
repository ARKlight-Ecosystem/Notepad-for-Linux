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
