# Backend

The [Flask](https://flask.palletsprojects.com/) app that serves the
compiled ARKlight output, plus (starting Stage 4) everything a static
compiler can't do itself: reading and writing files on disk, and
anything else this editor needs that requires a real, running process.

## Status

Not Stage 4 or 5 yet -- no File-menu endpoint exists. What's here now
is narrower, and arrived ahead of schedule out of necessity: see
["A delivery-mechanism amendment"](../../docs/implementation/CLASSIC-SHELL-ADDENDUM.md#a-delivery-mechanism-amendment-pywebview-ahead-of-schedule)
in the addendum for the full reasoning. Short version -- a page in an
ordinary browser tab can't control its own window's
minimize/maximize/close/drag, and ARKlight's native desktop backend
isn't on `main` yet, so this folder carries a minimal Flask static
file server (`app.py`) and a [pywebview](https://pywebview.flowrl.com/)
launcher (`desktop.py`) that opens that served page in a real, native
OS window instead. The OS's own title bar stays on for now
(`frameless=False`) because the shell's drawn minimize/maximize/close
row is still Stage 1 cosmetic-only.

## What belongs here

- The Flask app and its routes.
- File-system access and any other operation that genuinely needs a
  live process, scoped to whatever the current addendum stage
  actually asks for -- not a general-purpose API surface built ahead
  of need.
- `desktop.py`'s native-window wrapper, until ARKlight's own desktop
  backend makes it redundant (see Stage 5 of the addendum).

## What doesn't

- Anything ARKlight can already express as compiled static output --
  that's [`src/frontend/`](../frontend/README.md)'s job.

## Layout

- `app.py` -- `create_app()`, a Flask app that serves
  `src/frontend/ARK/` (the `arklight build` output) as static files.
  No File-menu routes yet; that's Stage 4.
- `desktop.py` -- runs `app.py` in a background thread, then opens it
  in a native pywebview window instead of a browser tab.
- `requirements.txt` -- `flask`, `pywebview`. Interim-delivery
  dependencies, not a Stage 4/5 commitment -- `pywebview` in
  particular may not survive Stage 5, per the addendum.

## Running it

```sh
cd src/frontend && ARKLIGHT_ACCEPT_LICENSE=1 arklight build site.py --no-open
cd ../backend && pip install -r requirements.txt
python desktop.py
```
