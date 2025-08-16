from ignis.widgets import Widget
from . import logic


def widget(self):
    Widget.Window(
        namespace="homescreen IGNIS",
        anchor=["bottom"],
        child=Widget.Box(
            vertical=True,
            child=[
                Widget.Label(
                    label=self.time.bind("value"),
                    css_classes=["homescreen", "time"],
                    halign="center",
                ),
                Widget.Label(
                    label=self.day.bind("value"),
                    css_classes=["homescreen", "day"],
                    halign="center",
                ),
            ],
            css_classes=["homescreen", "box"],
        ),
        layer="bottom",
    )


def main():
    data = logic.DATA()
    widget(data)
