# include <stdlib.ARKlight>

"""The classic Notepad++ window chrome -- Stage 1 (static shell) and
Stage 2 (File menu opens/closes) of
docs/implementation/CLASSIC-SHELL-ADDENDUM.md. Everything except
`menu_bar()`'s File item and its dropdown is still exactly Stage 1:
hard-coded, no `State`, no `on_click`. File is the one piece of
interactivity this file carries, and deliberately the only one --
every other menu-bar label stays a plain, inert `Span`.

`register_styles(site)` must be called once, before any page that
uses these components is built (see site.py) -- it's where every
`np-*` class below actually gets its rules, via `site.style(...)`.
"""

from content.site_content import (
    FILE_MENU_ITEMS,
    GUTTER_LINE_COUNT,
    MENU_LABELS,
    STATUS_SEGMENTS,
    TABS,
    TOOLBAR_GROUPS,
)

FONT_STACK = '"Segoe UI", Tahoma, "MS Shell Dlg 2", sans-serif'


def register_styles(site):
    """All Stage 1 shell styling, registered once against `site`."""

    site.style("np-window", {
        "display": "flex",
        "flex-direction": "column",
        "height": "100vh",
        "font-family": FONT_STACK,
        "font-size": "12px",
        "color": "#1a1a1a",
        "background": "#ffffff",
        "border": "1px solid #b0b0b0",
        "overflow": "hidden",
    })

    # -- Title bar ----------------------------------------------------
    site.style("np-titlebar", {
        "display": "flex",
        "align-items": "center",
        "justify-content": "space-between",
        "height": "30px",
        "flex": "0 0 auto",
        "background": "#ffffff",
        "border-bottom": "1px solid #e2e2e2",
        "padding-left": "8px",
    })
    site.style("np-titlebar-left", {
        "display": "flex",
        "align-items": "center",
        "gap": "6px",
        "min-width": "0",
    })
    site.style("np-titlebar-icon", {
        "width": "16px",
        "height": "16px",
        "flex": "0 0 auto",
    })
    site.style("np-titlebar-text", {
        "font-size": "12px",
        "white-space": "nowrap",
        "overflow": "hidden",
        "text-overflow": "ellipsis",
    })
    site.style("np-titlebar-controls", {
        "display": "flex",
        "height": "100%",
    })
    site.style("np-titlebar-btn", {
        "width": "46px",
        "height": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
        "font-size": "10px",
        "color": "#1a1a1a",
        ":hover:background": "#e5e5e5",
    })
    site.style("np-titlebar-btn-close", {
        ":hover:background": "#e81123",
        ":hover:color": "#ffffff",
    })

    # -- Menu bar -------------------------------------------------------
    site.style("np-menubar", {
        "display": "flex",
        "align-items": "center",
        "flex": "0 0 auto",
        "height": "24px",
        "background": "#f3f3f3",
        "border-bottom": "1px solid #d9d9d9",
        "padding-left": "4px",
        "font-size": "12.5px",
        "position": "relative",
        "z-index": "20",
    })
    site.style("np-menu-item", {
        "padding": "2px 8px",
        "border-radius": "2px",
        ":hover:background": "#cce4f7",
    })
    site.style("np-menu-file", {
        "position": "relative",
    })

    # -- File dropdown (Stage 2) -------------------------------------------
    site.style("np-menu-backdrop", {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "right": "0",
        "bottom": "0",
        "z-index": "10",
        "background": "transparent",
    })
    site.style("np-file-dropdown", {
        "position": "absolute",
        "top": "100%",
        "left": "0",
        "z-index": "30",
        "min-width": "260px",
        "padding": "4px 0",
        "background": "#ffffff",
        "border": "1px solid #c6c6c6",
        "box-shadow": "2px 2px 6px rgba(0, 0, 0, 0.18)",
    })
    site.style("np-file-item", {
        "display": "flex",
        "align-items": "center",
        "justify-content": "space-between",
        "gap": "24px",
        "padding": "4px 20px 4px 28px",
        "white-space": "nowrap",
        ":hover:background": "#cce4f7",
    })
    site.style("np-file-item-hint", {
        "color": "#888888",
        "font-size": "11px",
    })
    site.style("np-file-sep", {
        "border": "none",
        "border-top": "1px solid #e4e4e4",
        "margin": "4px 8px",
    })

    # -- Toolbar ----------------------------------------------------------
    site.style("np-toolbar", {
        "display": "flex",
        "align-items": "center",
        "flex": "0 0 auto",
        "height": "28px",
        "background": "#f3f3f3",
        "border-bottom": "1px solid #d9d9d9",
        "padding": "0 4px",
        "gap": "6px",
    })
    site.style("np-toolbar-group", {
        "display": "flex",
        "gap": "2px",
    })
    site.style("np-toolbar-icon", {
        "width": "20px",
        "height": "20px",
        "border-radius": "3px",
        "background": "#d8d8d8",
        "border": "1px solid #c3c3c3",
        ":hover:background": "#cce4f7",
        ":hover:border-color": "#99ccee",
    })
    site.style("np-toolbar-divider", {
        "width": "1px",
        "align-self": "stretch",
        "margin": "4px 0",
        "background": "#d0d0d0",
    })

    # -- Tab strip --------------------------------------------------------
    site.style("np-tabstrip", {
        "display": "flex",
        "align-items": "flex-end",
        "flex": "0 0 auto",
        "height": "26px",
        "background": "#e4e4e4",
        "border-bottom": "1px solid #d9d9d9",
        "padding-left": "4px",
        "gap": "2px",
    })
    site.style("np-tab", {
        "display": "flex",
        "align-items": "center",
        "gap": "6px",
        "height": "22px",
        "padding": "0 8px",
        "font-size": "12px",
        "background": "#dcdcdc",
        "border": "1px solid #d0d0d0",
        "border-bottom": "none",
    })
    site.style("np-tab-active", {
        "background": "#ffffff",
        "border-top": "2px solid #ff8800",
    })
    site.style("np-tab-close", {
        "width": "14px",
        "height": "14px",
        "text-align": "center",
        "line-height": "14px",
        "border-radius": "2px",
        ":hover:background": "#d0453c",
        ":hover:color": "#ffffff",
    })

    # -- Editor body: gutter + pane ----------------------------------------
    site.style("np-body", {
        "flex": "1 1 auto",
        "display": "flex",
        "min-height": "0",
        "background": "#ffffff",
    })
    site.style("np-gutter", {
        "flex": "0 0 auto",
        "width": "36px",
        "padding": "4px 6px 4px 0",
        "background": "#ffffff",
        "color": "#8a8a8a",
        "text-align": "right",
        "font-family": '"Consolas", "Courier New", monospace',
        "font-size": "13px",
        "line-height": "18px",
        "user-select": "none",
    })
    site.style("np-gutter-line", {"display": "block"})
    site.style("np-editor", {
        "flex": "1 1 auto",
        "border": "none",
        "outline": "none",
        "resize": "none",
        "padding": "4px 8px",
        "font-family": '"Consolas", "Courier New", monospace',
        "font-size": "13px",
        "line-height": "18px",
        "color": "#1a1a1a",
    })

    # -- Status bar ---------------------------------------------------------
    site.style("np-statusbar", {
        "display": "flex",
        "align-items": "center",
        "justify-content": "flex-end",
        "flex": "0 0 auto",
        "height": "22px",
        "background": "#f3f3f3",
        "border-top": "1px solid #d9d9d9",
        "font-size": "11.5px",
        "color": "#3a3a3a",
    })
    site.style("np-status-segment", {
        "padding": "0 10px",
        "border-left": "1px solid #d9d9d9",
        "height": "100%",
        "display": "flex",
        "align-items": "center",
        "white-space": "nowrap",
    })


# ---------------------------------------------------------------------------
# Markup
# ---------------------------------------------------------------------------


def title_bar(title):
    return Container(
        Container(
            Image(src="assets/icon.svg", class_name="np-titlebar-icon"),
            Span(title, class_name="np-titlebar-text"),
            class_name="np-titlebar-left",
        ),
        Container(
            Span("\u2212", class_name="np-titlebar-btn"),   # minimize
            Span("\u25a1", class_name="np-titlebar-btn"),   # maximize
            Span("\u00d7", class_name="np-titlebar-btn np-titlebar-btn-close"),
            class_name="np-titlebar-controls",
        ),
        class_name="np-titlebar",
    )


def file_dropdown():
    rows = []
    for item in FILE_MENU_ITEMS:
        if item.get("separator"):
            rows.append(HorizontalRule(class_name="np-file-sep"))
            continue
        if item.get("submenu"):
            hint = "\u25b8"
            row = Container(
                Span(item["label"], class_name="np-file-item-label"),
                Span(hint, class_name="np-file-item-hint"),
                class_name="np-file-item",
            )
        else:
            hint = item.get("shortcut", "")
            row = Container(
                Span(item["label"], class_name="np-file-item-label"),
                Span(hint, class_name="np-file-item-hint"),
                class_name="np-file-item",
                # No real New/Open/Save/... behavior yet (Stage 4) --
                # clicking an item just closes the dropdown, the same
                # way a real menu would, without claiming to do the
                # file operation it's labeled for.
                on_click=Action.set("file_menu_open", False),
            )
        rows.append(row)
    return Container(*rows, class_name="np-file-dropdown")


def menu_bar():
    file_item = Container(
        Span("File", class_name="np-menu-item", on_click=Action.toggle_bool("file_menu_open")),
        Show(Predicate.truthy("file_menu_open"), file_dropdown()),
        class_name="np-menu-file",
    )
    other_items = [Span(label, class_name="np-menu-item") for label in MENU_LABELS[1:]]
    # Full-viewport click-catcher, shown only while the dropdown is
    # open, stacked below the menu bar (z-index 10 vs. 20) so a click
    # back on "File" itself still reaches File's own `on_click`
    # instead of the backdrop -- the "click outside closes it" half of
    # Stage 2's done-when criterion. There's no Escape-key equivalent:
    # ARKlight has no keydown/key-press primitive yet, so that half of
    # the addendum's original Stage 2 wording is deferred, not faked --
    # see the addendum's Stage 2 section for the amendment.
    backdrop = Show(
        Predicate.truthy("file_menu_open"),
        Container(class_name="np-menu-backdrop", on_click=Action.set("file_menu_open", False)),
    )
    return Container(file_item, *other_items, backdrop, class_name="np-menubar")


def toolbar():
    groups = []
    for group in TOOLBAR_GROUPS:
        groups.append(Container(
            *[Span(class_name="np-toolbar-icon", **{"data-icon": name}) for name in group],
            class_name="np-toolbar-group",
        ))
    # interleave a divider between groups, none trailing
    children = []
    for i, group in enumerate(groups):
        if i:
            children.append(Span(class_name="np-toolbar-divider"))
        children.append(group)
    return Container(*children, class_name="np-toolbar")


def tab_strip():
    tabs = []
    for tab in TABS:
        classes = "np-tab np-tab-active" if tab["active"] else "np-tab"
        tabs.append(Container(
            Span(tab["label"]),
            Span("\u00d7", class_name="np-tab-close"),
            class_name=classes,
        ))
    return Container(*tabs, class_name="np-tabstrip")


def editor_area():
    gutter_lines = [
        Span(str(n), class_name="np-gutter-line")
        for n in range(1, GUTTER_LINE_COUNT + 1)
    ]
    return Container(
        Container(*gutter_lines, class_name="np-gutter"),
        Textarea("", class_name="np-editor"),
        class_name="np-body",
    )


def status_bar():
    return Container(
        *[Span(seg, class_name="np-status-segment") for seg in STATUS_SEGMENTS],
        class_name="np-statusbar",
    )
