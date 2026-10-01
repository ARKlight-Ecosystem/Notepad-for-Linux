"""Classic-shell content -- Stage 1 (hard-coded values) and Stage 3
(which of them stay hard-coded) of
docs/implementation/CLASSIC-SHELL-ADDENDUM.md. Still no real filename
and no real document: every value is a plausible default, the same
way the reference screenshot's own Notepad++ window would look with a
single untitled, unmodified tab. Stage 3 replaced exactly two status-
bar values (length, lines) with live ones -- see `STATUS_SEGMENTS`.
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

# Toolbar icons that map to a File-menu action and are therefore
# clickable as of Stage 3. They fire the same placeholder handler the
# matching File-menu rows do (`shell.file_placeholder_action()`), so
# the toolbar and the menu can't disagree. Every other icon belongs to
# a menu (Edit, Search, View, ...) that is still out of scope, so it
# stays inert -- `save-all`, `close` and `print` are File-menu actions
# too, but the addendum only names new/open/save for this stage.
TOOLBAR_FILE_ACTIONS = {"new", "open", "save"}

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

# Tab strip -- a single hard-coded tab, styled active. Stage 3 gives
# its close (x) a working click: there is no document lifecycle yet,
# so closing the only tab shows this placeholder notice instead of
# doing anything destructive. (Silently resetting the editor would
# throw away typed text with none of Notepad++'s save prompt.)
TABS = [{"label": "new 1", "active": True}]
CLOSE_TAB_NOTICE = "Closing the last tab isn't wired up yet \u2014 there is no real document to close."

# Status bar segments, left to right, same order as the reference
# screenshot. A plain string is a hard-coded default for an empty,
# untitled document. A dict is Stage 3's live field: `prefix` is the
# static label and `computed` names a `Computed(...)` declared on the
# page in `pages/home.py`, derived from the editor's text.
#
# Only length and lines are live. Ln/Col/Pos (and selection length)
# need the caret/selection offsets, and ARKlight's closed vocabulary has
# no primitive that exposes them (a script extension could, but this
# project doesn't use one) -- tracked as a gap in the addendum's Stage 3
# amendment, not faked (e.g. by assuming the caret is at the end of the
# text).
# Encoding, EOL style and file type need a real file: Stage 4/5.
STATUS_SEGMENTS = [
    "Normal text file",
    {"prefix": "length : ", "computed": "doc_length"},
    {"prefix": "lines : ", "computed": "doc_lines"},
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
