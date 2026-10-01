# include <stdlib.ARKlight>

from components.shell import editor_area, menu_bar, status_bar, tab_strip, title_bar, toolbar
from content.site_content import APP_TITLE, FAVICON, PAGE_DESCRIPTION, PAGE_TITLE


def home():
    return Page(
        State("file_menu_open", False),
        # Stage 3: the editor's text, two-way bound to the textarea,
        # and the status-bar fields derived from it. Ln/Col/Pos are
        # deliberately not here -- see STATUS_SEGMENTS.
        State("editor_text", ""),
        State("close_tab_notice", False),
        Computed("doc_length", deps=("editor_text",), derive=Derive.string_length("editor_text")),
        Computed("doc_lines", deps=("editor_text",), derive=Derive.split_count("editor_text", "\n")),
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
