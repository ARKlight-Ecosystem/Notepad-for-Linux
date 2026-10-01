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


def test_assets_are_copied_into_the_build(built):
    assert (built / "assets" / "icon.svg").exists()
