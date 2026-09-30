# include <stdlib.ARKlight>


@component(props={"active": Prop(default=None)})
def NavBar(active=None):
    """The shared nav bar. `active` is one of "home"/"about" -- pass it
    from each page so the current link gets highlighted."""
    return Container(
        Link("Home", href="/", class_name="active" if active == "home" else None),
        Link("About", href="/about", class_name="active" if active == "about" else None),
        class_name="nav",
    )
