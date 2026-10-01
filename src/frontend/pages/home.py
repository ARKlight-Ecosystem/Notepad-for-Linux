# include <stdlib.ARKlight>

from components.shell import editor_area, menu_bar, status_bar, tab_strip, title_bar, toolbar
from content.site_content import APP_TITLE, FAVICON, PAGE_DESCRIPTION, PAGE_TITLE


def home():
    return Page(
        State("file_menu_open", False),
        Container(
            title_bar(APP_TITLE),
            menu_bar(),
            toolbar(),
            tab_strip(),
            editor_area(),
            status_bar(),
            class_name="np-window",
        ),
        title=PAGE_TITLE,
        description=PAGE_DESCRIPTION,
        favicon=FAVICON,
    )
