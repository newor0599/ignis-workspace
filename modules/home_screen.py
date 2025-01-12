from ignis.widgets import Widget
from ignis.utils import Utils
import datetime

one_min = 1000 * 60
clock = Widget.Label(
    label="Hello!",
    valign="center",
    halign="center",
    css_classes=["homescreen", "clock"],
)


def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)


Utils.Poll(timeout=one_min, callback=lambda x: update_clock())


def home_screen(monitor: int = 0):
    return Widget.Window(
        monitor=monitor,
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
