"""Hard-coded classic-shell content -- Stage 1 of
docs/implementation/CLASSIC-SHELL-ADDENDUM.md. Nothing here is dynamic
yet: no `State`, no real filename, no real document. Every value is a
plausible default, the same way the reference screenshot's own
Notepad++ window would look with a single untitled, unmodified tab.
"""

APP_TITLE = "new 1 - Notepad++"

# Page <title>/description/favicon -- unrelated to the in-window title
# bar text above, which is rendered as ordinary markup, not the real
# browser tab title (Stage 5 is the earliest this could mean anything
# more than a label).
PAGE_TITLE = "Notepad++"
PAGE_DESCRIPTION = "A native-feeling Notepad++ experience for Linux."
FAVICON = "assets/icon.svg"

# Menu bar, left to right -- classic order, File first. None of these
# open anything yet; Stage 2 gives File a working dropdown and leaves
# the other twelve exactly this inert.
MENU_LABELS = [
    "File", "Edit", "Search", "View", "Encoding", "Language",
    "Settings", "Tools", "Macro", "Run", "Plugins", "Window", "?",
]

# File dropdown, Stage 2 -- classic Notepad++ order and grouping.
# `shortcut`: commonly-known defaults (New/Open/Save/Save As/Close/
# Print/Exit) -- not independently checked against a live Notepad++
# install, left blank rather than guessed where uncertain. `submenu`:
# renders a `\u25b8` disclosure glyph instead of a shortcut; Recent
# Files doesn't get a real submenu this stage (out of scope -- see
# the addendum), just the classic affordance, and gets no `on_click`
# so it can't pretend to do something it doesn't.
FILE_MENU_ITEMS = [
    {"label": "New", "shortcut": "Ctrl+N"},
    {"label": "New Window", "shortcut": ""},
    {"separator": True},
    {"label": "Open...", "shortcut": "Ctrl+O"},
    {"label": "Open Folder...", "shortcut": ""},
    {"label": "Open in Explorer", "shortcut": ""},
    {"label": "Reload", "shortcut": ""},
    {"separator": True},
    {"label": "Save", "shortcut": "Ctrl+S"},
    {"label": "Save As...", "shortcut": "Ctrl+Alt+S"},
    {"label": "Save a Copy As...", "shortcut": ""},
    {"label": "Save All", "shortcut": ""},
    {"label": "Rename", "shortcut": ""},
    {"separator": True},
    {"label": "Close", "shortcut": "Ctrl+W"},
    {"label": "Close All", "shortcut": ""},
    {"label": "Close All but Current", "shortcut": ""},
    {"separator": True},
    {"label": "Recent Files", "submenu": True},
    {"separator": True},
    {"label": "Print", "shortcut": "Ctrl+P"},
    {"label": "Print Now", "shortcut": ""},
    {"separator": True},
    {"label": "Exit", "shortcut": "Alt+F4"},
]

# Toolbar icon strip, left to right, grouped the way the reference
# screenshot groups them (a gap marks a divider). Stage 1 draws these
# as plain static placeholders -- real icon artwork is a later pass,
# not a Stage 1 concern (the addendum only asks for "the classic icon
# strip ... rendered as static icons in the reference layout").
TOOLBAR_GROUPS = [
    ["new", "open", "save", "save-all"],
    ["close", "print"],
    ["cut", "copy", "paste"],
    ["undo", "redo"],
    ["find", "find-in-files"],
    ["zoom-in", "zoom-out"],
    ["wrap", "all-chars"],
]

# Tab strip -- a single hard-coded tab, styled active. Closing it is a
# Stage 3 concern (and even then, a no-op/placeholder -- see the
# addendum).
TABS = [{"label": "new 1", "active": True}]

# Status bar segments, left to right, same order as the reference
# screenshot. Values are plausible defaults for an empty, untitled
# document -- not computed from anything real yet.
STATUS_SEGMENTS = [
    "Normal text file",
    "length : 0",
    "lines : 1",
    "Ln : 1",
    "Col : 1",
    "Pos : 1",
    "Windows (CR LF)",
    "UTF-8",
    "INS",
]

# Line-number gutter row count for the empty editor pane -- enough to
# fill a typical window height without real document content yet.
GUTTER_LINE_COUNT = 24
