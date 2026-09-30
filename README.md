# Notepad++ for Linux

A native-feeling Notepad++ experience for Linux, built as a local
web app: an [ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight)
frontend (Python-in, HTML-out -- no hand-written JavaScript) served by
a small Flask backend that does the actual file-system and editing
work. [`notepad-plus-plus-reference/`](notepad-plus-plus-reference/)
is the upstream Notepad++ source, vendored read-only as a behavior and
feature reference -- not something this project builds or ships.

## Status

Early scaffolding. No app code yet -- this commit initializes the
documentation lifecycle the project will use as it grows. See
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

## Documentation

Start at [`docs/README.md`](docs/README.md). This project follows the
same documentation lifecycle ARKlight itself uses -- see that file for
the full explanation of `docs/foundational/`, `docs/implementation/`,
and `docs/proposal/`.

## License

See [`LICENSE`](LICENSE).
