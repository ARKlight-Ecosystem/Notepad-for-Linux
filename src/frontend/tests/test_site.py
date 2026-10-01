"""Build smoke tests. Run with `pytest` (`pip install pytest` first).

They build the real site into a temp directory, so a broken import, a
misspelled component, a missing required prop, or an undeclared state
name fails here in milliseconds instead of at deploy time. Add a route
to site.py -> add its output file to ROUTES.
"""

from pathlib import Path

import pytest

from arklight.compiler.pipeline import build

SITE = Path(__file__).resolve().parent.parent / "site.py"

# route -> the file `arklight build` writes for it. Stage 1 of
# docs/implementation/CLASSIC-SHELL-ADDENDUM.md is one route, one
# window -- this isn't a marketing site with pages to add.
ROUTES = {"/": "index.html"}


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("ARK")
    build(SITE, out_dir)
    return out_dir


@pytest.mark.parametrize("output_file", ROUTES.values())
def test_every_route_builds(built, output_file):
    assert (built / output_file).exists()


def test_classic_shell_regions_are_present(built):
    """One assertion per region Stage 1 claims to render -- same
    regions, same order the reference screenshot has, per the
    addendum's own 'Done when' criterion for this stage."""
    html = (built / "index.html").read_text(encoding="utf-8")
    regions = [
        "np-titlebar",
        "np-menubar",
        "np-toolbar",
        "np-tabstrip",
        "np-body",
        "np-gutter",
        "np-editor",
        "np-statusbar",
    ]
    positions = [html.index(f'class="{r}' if r != "np-editor" else 'class="np-editor') for r in regions]
    assert positions == sorted(positions), "shell regions are out of the reference screenshot's order"


def test_all_thirteen_menus_present_in_order(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    expected = [
        "File", "Edit", "Search", "View", "Encoding", "Language",
        "Settings", "Tools", "Macro", "Run", "Plugins", "Window", "?",
    ]
    positions = [html.index(f">{label}<") for label in expected]
    assert positions == sorted(positions), "menu bar labels are out of classic order"


def test_file_menu_toggles_open_and_the_other_twelve_stay_inert(built):
    """Stage 2's actual 'done when': File has real on_click wiring,
    everything else is still a plain inert label (no `data-ark-*`
    attribute at all)."""
    html = (built / "index.html").read_text(encoding="utf-8")
    assert 'data-ark-on-click="action:toggle_bool"' in html
    assert 'data-ark-action-state="file_menu_open"' in html
    for label in ["Edit", "Search", "View", "Encoding", "Language",
                  "Settings", "Tools", "Macro", "Run", "Plugins",
                  "Window", "?"]:
        i = html.index(f'>{label}<')
        tag_start = html.rindex("<span", 0, i)
        tag = html[tag_start:i]
        assert "data-ark-" not in tag, f"{label!r} should still be inert in Stage 2"


def test_file_dropdown_has_all_items_in_classic_order(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    expected_labels = [
        "New", "New Window", "Open...", "Open Folder...",
        "Open in Explorer", "Reload", "Save", "Save As...",
        "Save a Copy As...", "Save All", "Rename", "Close",
        "Close All", "Close All but Current", "Recent Files",
        "Print", "Print Now", "Exit",
    ]
    positions = [html.index(f'>{label}<') for label in expected_labels]
    assert positions == sorted(positions), "File dropdown items are out of classic order"


def test_recent_files_has_no_click_behavior(built):
    """Recent Files is a submenu affordance only (Stage 2 doesn't
    build real nested submenus) -- it must not claim to close the
    menu or do anything else on click."""
    html = (built / "index.html").read_text(encoding="utf-8")
    i = html.index(">Recent Files<")
    tag_start = html.rindex("<div", 0, i)
    tag = html[tag_start:i]
    assert "data-ark-" not in tag


def test_backdrop_closes_the_menu_and_is_gated_by_the_same_state(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    i = html.index("np-menu-backdrop")
    tag = html[max(0, i - 40):i + 200]
    assert 'data-ark-on-click="action:set"' in tag
    assert 'data-ark-action-state="file_menu_open"' in tag
    assert '&quot;value&quot;: false' in tag


# -- Stage 3: toolbar, tabs, status bar ---------------------------------


def _icon_tag(html, name):
    i = html.index(f'data-icon="{name}"')
    start = html.rindex("<span", 0, i)
    return html[start:html.index(">", i)]


def test_new_open_save_toolbar_icons_route_to_the_same_handler_as_the_menu(built):
    """The toolbar and the File menu must agree: each of new/open/save
    carries exactly the placeholder action every File-menu row does."""
    html = (built / "index.html").read_text(encoding="utf-8")
    for name in ("new", "open", "save"):
        tag = _icon_tag(html, name)
        assert 'data-ark-on-click="action:set"' in tag, name
        assert 'data-ark-action-state="file_menu_open"' in tag, name
        assert "&quot;value&quot;: false" in tag, name


def test_other_toolbar_icons_stay_inert(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    # Spelled out here on purpose (not imported from content/): the
    # test should fail if an icon gains behavior the addendum doesn't ask for.
    inert = ["save-all", "close", "print", "cut", "copy", "paste", "undo",
             "redo", "find", "find-in-files", "zoom-in", "zoom-out",
             "wrap", "all-chars"]
    for name in inert:
        assert "data-ark-" not in _icon_tag(html, name), f"{name!r} should stay inert in Stage 3"


def test_tab_close_opens_a_placeholder_notice_that_can_be_dismissed(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    i = html.index("np-tab-close")
    close_tag = html[html.rindex("<span", 0, i):html.index(">", i)]
    assert 'data-ark-action-state="close_tab_notice"' in close_tag
    assert "&quot;value&quot;: true" in close_tag
    j = html.index("np-tab-notice-ok")
    ok_tag = html[html.rindex("<span", 0, j):html.index(">", j)]
    assert 'data-ark-action-state="close_tab_notice"' in ok_tag
    assert "&quot;value&quot;: false" in ok_tag
    # The notice itself is Show-gated on the same state key.
    assert "close_tab_notice" in html[html.rindex("<div", 0, html.index("np-tab-notice\"")):]


def test_editor_is_two_way_bound_and_status_fields_are_live(built):
    html = (built / "index.html").read_text(encoding="utf-8")
    assert 'data-ark-model="editor_text"' in html
    assert 'data-ark-bind="doc_length"' in html
    assert 'data-ark-bind="doc_lines"' in html
    # Empty-document defaults still render (what a JS-disabled page shows).
    assert 'length : <span data-ark-bind="doc_length">0</span>' in html
    assert 'lines : <span data-ark-bind="doc_lines">1</span>' in html


def test_fields_that_need_a_caret_or_a_file_stay_hard_coded(built):
    """Ln/Col/Pos need caret offsets the closed vocabulary can't expose; encoding/EOL
    need a real file. None of them may be bound to anything."""
    html = (built / "index.html").read_text(encoding="utf-8")
    for text in ("Normal text file", "Ln : 1", "Col : 1", "Pos : 1",
                 "Windows (CR LF)", "UTF-8", "INS"):
        i = html.index(f">{text}<")
        tag = html[html.rindex("<span", 0, i):i]
        assert "data-ark-" not in tag, f"{text!r} should stay hard-coded in Stage 3"


def test_assets_are_copied_into_the_build(built):
    assert (built / "assets" / "icon.svg").exists()
