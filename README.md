# Notepad++ for Linux

A native-feeling Notepad++ experience for Linux, built as a local
web app: an [ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight)
frontend (Python-in, HTML-out -- no hand-written JavaScript) served by
a small Flask backend that does the actual file-system and editing
work. [`notepad-plus-plus-reference/`](notepad-plus-plus-reference/)
is the upstream Notepad++ source, vendored read-only as a behavior and
feature reference -- not something this project builds or ships.

## Status

Stage 1 of the classic shell is shipped -- see
[`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`](docs/implementation/CLASSIC-SHELL-ADDENDUM.md).
`src/frontend/` builds a static, pixel-checked match for the classic
Notepad++ window chrome; `src/backend/` serves it in a real native
window via Flask + pywebview, an interim stand-in for ARKlight's own
desktop backend (not on `main` yet). Nothing is interactive or reads/
writes a real file yet -- that's Stages 2 onward. See
[`docs/README.md`](docs/README.md) for where things live and why.

## Stack

- **Frontend** -- [ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight),
  a Python-first compiler: you write Python (`Site`, `Page`,
  components), it compiles to plain, dependency-free HTML/CSS/JS. No
  JavaScript is hand-written; ARKlight's closed component/behavior
  vocabulary is the entire client-side surface.
- **Backend** -- [Flask](https://flask.palletsprojects.com/), serving
  the compiled ARKlight output and handling everything that needs a
  real process: reading/writing files on disk, search, and whatever
  else a text editor needs that a static compiler can't do alone.
- **Native window (interim)** -- [pywebview](https://pywebview.flowrl.com/)
  opens the Flask-served output in a real OS window instead of a
  browser tab, so the classic shell's title bar can eventually control
  an actual window. A stand-in for ARKlight's own native desktop
  backend until that ships -- see
  [`src/backend/README.md`](src/backend/README.md).

## Documentation

Start at [`docs/README.md`](docs/README.md). This project follows the
same documentation lifecycle ARKlight itself uses -- see that file for
the full explanation of `docs/foundational/`, `docs/implementation/`,
and `docs/proposal/`.

## License

See [`LICENSE`](LICENSE).
