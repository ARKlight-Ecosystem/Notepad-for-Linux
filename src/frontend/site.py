# include <stdlib.ARKlight>

from pages.about import about
from pages.home import home

site = Site()


# Real @site.page(...) decorators live here, not in pages/*.py --
# static discovery (arklight.parser.discover) only looks at the entry
# file's own source, so this is the one place routes must be declared.
# Each function below just delegates to the actual page-content
# function in pages/, which is free to import components/ and
# content/ however it likes.


@site.page("/")
def home_page():
    return home()


@site.page("/about")
def about_page():
    return about()
