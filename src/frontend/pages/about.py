# include <stdlib.ARKlight>

from components.footer import footer
from components.nav import NavBar
from content.site_content import DESCRIPTION, FAVICON, TITLE


def about():
    return Page(
        NavBar(active="about"),
        Heading("About", level=2),
        Text(f"Say something about {TITLE} here."),
        Link("Back home", href="/"),
        footer(),
        title="About",
        description=DESCRIPTION,
        favicon=FAVICON,
    )
