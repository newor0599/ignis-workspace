from ignis.widgets import Widget
from ignis.utils import Utils
import datetime

clock_rate = 1000 * 20
clock = Widget.Label(
    label="Hello!",
    valign="center",
    halign="center",
    css_classes=["homescreen", "clock"],
)


def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)


Utils.Poll(timeout=clock_rate, callback=lambda x: update_clock())


def home_screen(monitor: int = 0) -> Widget.Window:
    return Widget.Window(
        monitor=monitor,
        anchor=["bottom", "right"],
        namespace="Home Screen",
        exclusivity="normal",
        layer="bottom",
        css_classes=["homescreen", "window"],
        child=Widget.Box(
            child=[
                clock,
            ],
        ),
    )
