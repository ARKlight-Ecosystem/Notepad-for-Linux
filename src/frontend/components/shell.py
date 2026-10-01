# include <stdlib.ARKlight>

"""The classic Notepad++ window chrome -- Stage 1 of
docs/implementation/CLASSIC-SHELL-ADDENDUM.md: a static match for the
reference screenshot, no `State`, no `on_click`, nothing dynamic.
Stage 2 gives the File menu a working dropdown; Stage 3 wakes up the
toolbar/tabs/status-bar fields that can be computed client-side. Both
build directly on the markup and class names below, so names here are
picked to still make sense once they do.

`register_styles(site)` must be called once, before any page that
uses these components is built (see site.py) -- it's where every
`np-*` class below actually gets its rules, via `site.style(...)`.
"""

from content.site_content import (
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
    })
    site.style("np-menu-item", {
        "padding": "2px 8px",
        "border-radius": "2px",
        ":hover:background": "#cce4f7",
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


def menu_bar():
    return Container(
        *[Span(label, class_name="np-menu-item") for label in MENU_LABELS],
        class_name="np-menubar",
    )


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
