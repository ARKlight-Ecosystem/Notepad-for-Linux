# Frontend

This is where the [ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight)
source lives -- the `Site`/`Page`/component Python that compiles down
to the plain, dependency-free HTML/CSS/JS the app actually ships.
Nothing here is hand-written JavaScript; if a piece of UI needs
client-side behavior, it's expressed through ARKlight's
`State`/`Bind`/`Action` vocabulary, not a `<script>` tag.

## Status

Stages 1 and 2 of
[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](../../docs/implementation/CLASSIC-SHELL-ADDENDUM.md)
are shipped: `arklight build site.py` produces a classic Notepad++
shell -- title bar, menu bar, toolbar, tab strip, editor pane with
line-number gutter, status bar -- matching the reference screenshot's
regions, order, and proportions, with a working File dropdown (opens
on click, closes on an outside click, items in classic order with
shortcut hints). The other twelve menu-bar labels are still inert;
that's a future addendum each.

## What belongs here

- ARKlight `Page`/component source for the app's UI.
- Nothing that reads or writes a real file, touches the filesystem, or
  needs a live process running -- that's `src/backend/`'s job, wired
  in through `on_click` targets once Stage 4 of the addendum exists.

## Layout

- `site.py` -- the one route (`/`) this app has.
- `pages/home.py` -- composes the shell into a `Page`.
- `components/shell.py` -- the shell itself: `title_bar`, `menu_bar`,
  `toolbar`, `tab_strip`, `editor_area`, `status_bar`, plus
  `register_styles(site)`, which must run once before any page using
  these is built (see `site.py`).
- `content/site_content.py` -- every hard-coded value the shell
  currently renders (menu labels, toolbar groups, status segments,
  tab list), named and commented so later stages know exactly what
  they're replacing with real state.
- `tests/test_site.py` -- build smoke tests: every route builds, the
  eight shell regions appear in the reference screenshot's order, and
  all thirteen menu labels are present and correctly ordered.
- `ARK/` -- build output (`arklight build site.py`), gitignored, not
  committed.

## Building it

```sh
cd src/frontend
ARKLIGHT_ACCEPT_LICENSE=1 arklight build site.py --no-open
```

(`ARKLIGHT_ACCEPT_LICENSE=1` is only needed non-interactively, e.g. in
CI -- an interactive `arklight build` asks once and remembers.) See
[`src/backend/README.md`](../backend/README.md) for how this build
output actually gets opened as a window right now.
