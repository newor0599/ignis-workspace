from ignis.widgets import Widget


def main():
    Widget.Window(
        namespace="watermark IGNIS",
        anchor=["bottom", "right"],
        child=Widget.Box(
            vertical=True,
            child=[
                Widget.Label(
                    label="Activate Linux",
                    css_classes=["watermark", "main"],
                    halign="start",
                ),
                Widget.Label(
                    label="Go to Settings to activate linux.",
                    css_classes=["watermark", "mini"],
                    halign="start",
                ),
            ],
            css_classes=["watermark", "box"],
        ),
        layer="overlay",
        input_height=0,
        input_width=0,
    )
