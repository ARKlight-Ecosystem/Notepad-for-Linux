"""The Flask half of Stage 1's delivery story.

Scope note: nothing in `docs/implementation/CLASSIC-SHELL-ADDENDUM.md`
asked for a backend before Stage 4 -- File-menu endpoints are still
the first *real* backend work on that ladder, and this file doesn't
do any of that yet. What it does instead is narrower and comes first
out of necessity, not scope creep: ARKlight's own native desktop
backend (GTK3 + WebKit2GTK) isn't on `main` yet (see
`docs/implementation/CLASSIC-SHELL-ADDENDUM.md`'s feasibility note),
so the window chrome's minimize/maximize/close/drag can't be made to
actually do anything as long as this only runs as a page in a regular
browser tab. `desktop.py` (pywebview, in this same folder) is the
interim stand-in for that missing native backend -- a real OS window
around the same compiled output -- and this file is just what that
window points at: a static file server for `src/frontend`'s
`arklight build` output. Nothing here reads or writes a document yet.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, send_from_directory

# `arklight build`'s default output directory, sitting next to this
# file's sibling `../frontend/site.py`. Stage 5 of the addendum is
# what's expected to eventually make this configurable / part of a
# real build step instead of a hard-coded relative path.
BUILD_DIR = (Path(__file__).resolve().parent.parent / "frontend" / "ARK").resolve()


def create_app(build_dir: Path = BUILD_DIR) -> Flask:
    """Serve `build_dir` (an `arklight build` output folder) as-is.

    Deliberately dumb: no templating, no routes beyond static-file
    serving. Real File-menu endpoints (New/Open/Save/Save As/Exit)
    are Stage 4's job, not this file's, and get added here -- not
    replacing this function, alongside it -- when that stage starts.
    """
    if not (build_dir / "index.html").exists():
        raise FileNotFoundError(
            f"No build at {build_dir} -- run `arklight build site.py` "
            f"in src/frontend/ first (see src/frontend/README.md)."
        )

    app = Flask(__name__, static_folder=None)

    @app.route("/")
    def index():
        return send_from_directory(build_dir, "index.html")

    @app.route("/<path:filename>")
    def static_files(filename):
        return send_from_directory(build_dir, filename)

    return app


if __name__ == "__main__":
    # Plain-browser dev mode -- `python app.py`, then open the printed
    # URL yourself. `desktop.py` is the one that wraps this in an
    # actual native window; this entry point exists so the Flask half
    # can be sanity-checked on its own, same reasoning as
    # `src/frontend`'s own build-then-open-a-browser default.
    create_app().run(host="127.0.0.1", port=5175, debug=True)
