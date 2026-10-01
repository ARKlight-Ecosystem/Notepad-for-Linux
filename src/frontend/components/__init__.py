"""Reusable pieces shared across pages.

`shell.py` is the whole classic Notepad++ window chrome for Stage 1 of
docs/implementation/CLASSIC-SHELL-ADDENDUM.md -- title bar, menu bar,
toolbar, tab strip, editor pane, status bar -- plus `register_styles`,
which must be called once against `Site()` before any page using these
components is built (see site.py).
"""
