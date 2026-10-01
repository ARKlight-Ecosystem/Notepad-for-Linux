"""Interim native window: pywebview wrapping the Flask-served build.

Why this exists at all: the classic shell's title bar has real
minimize/maximize/close/drag semantics in the reference screenshot,
and a browser tab can't grant a page control over its own OS window
for those. ARKlight's own native desktop backend (GTK3 + WebKit2GTK)
is the eventual, correct answer -- and is explicitly not on `main`
yet. pywebview gets the same practical result today, with a
dependency this project wasn't otherwise carrying: a real OS-native
window (GTK/Qt on Linux, picking whichever is installed) around
ordinary local web content, with working native window chrome. This
is a delivery-mechanism decision, not a Stage 4/5 substitute -- File
still does nothing real until Stage 4 wires actual endpoints into
`app.py`.

Run with: `python desktop.py`, from `src/backend/`, after
`arklight build site.py` has produced `src/frontend/ARK/`.
"""

from __future__ import annotations

import threading

import webview

from app import BUILD_DIR, create_app

HOST = "127.0.0.1"
PORT = 5175


def _run_flask() -> None:
    # `use_reloader=False`: the reloader forks a second process, which
    # would open a second window alongside this one -- fine for `flask
    # run`'s own dev server, not fine wrapped in a single desktop app.
    create_app().run(host=HOST, port=PORT, debug=False, use_reloader=False)


def main() -> None:
    server = threading.Thread(target=_run_flask, daemon=True)
    server.start()

    # `frameless=False`, deliberately, even though the compiled shell
    # already draws its own title bar: that drawn title bar's
    # minimize/maximize/close row is still Stage 1 cosmetic-only (see
    # components/shell.py) -- nothing wires it to a real window action
    # yet. Going frameless now would trade "two title bars" for "zero
    # working ones." The OS decorations stay on until a later stage
    # wires the drawn buttons to `window.minimize()`/`toggle_fullscreen()`/
    # `destroy()` through pywebview's JS API, at which point this
    # flips to `frameless=True` in the same change.
    webview.create_window(
        "Notepad++",
        url=f"http://{HOST}:{PORT}/",
        width=1000,
        height=650,
        min_size=(640, 400),
        frameless=False,
    )
    webview.start()


if __name__ == "__main__":
    main()
