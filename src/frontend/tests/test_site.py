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

# route -> the file `arklight build` writes for it
ROUTES = {"/": "index.html", "/about": "about.html"}


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("ARK")
    build(SITE, out_dir)
    return out_dir


@pytest.mark.parametrize("output_file", ROUTES.values())
def test_every_route_builds(built, output_file):
    assert (built / output_file).exists()


def test_pages_share_the_nav_and_footer(built):
    for output_file in ROUTES.values():
        html = (built / output_file).read_text(encoding="utf-8")
        assert 'class="nav"' in html
        assert "<footer" in html


def test_assets_are_copied_into_the_build(built):
    assert (built / "assets" / "icon.svg").exists()
