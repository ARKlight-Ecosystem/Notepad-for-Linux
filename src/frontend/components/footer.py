# include <stdlib.ARKlight>

from content.site_content import FOOTER_TEXT


def footer():
    """A plain-function component: no registration needed."""
    return Footer(Text(FOOTER_TEXT, class_name="muted"))
