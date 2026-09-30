# include <stdlib.ARKlight>

from components.footer import footer
from components.nav import NavBar
from content.site_content import DESCRIPTION, FAVICON, TAGLINE, TITLE


def home():
    return Page(
        NavBar(active="home"),
        Heading(TITLE),
        Text(TAGLINE, class_name="muted"),
        footer(),
        title=TITLE,
        description=DESCRIPTION,
        favicon=FAVICON,
    )
