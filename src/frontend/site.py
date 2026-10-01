# include <stdlib.ARKlight>

from components.shell import register_styles
from pages.home import home

site = Site()
register_styles(site)


# Stage 1 of docs/implementation/CLASSIC-SHELL-ADDENDUM.md: one route,
# the classic shell itself. No `/about` -- this isn't a marketing site,
# it's a single-window desktop app, so there's exactly one page for now.
@site.page("/")
def home_page():
    return home()
