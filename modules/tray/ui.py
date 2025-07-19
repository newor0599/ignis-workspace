from ignis.widgets import Widget
from . import chips
from . import menus
from . import hitboxes
from . import logic


class BAR(hitboxes.BAR, menus.BAR, chips.BAR, logic.BAR):
    def tray(self):
        chips = Widget.Box(
            child=[self.ClockChip(), self.DateChip(), self.BatteryChip()],
            # halign="end",
            vexpand=True,
            css_classes=["chip-main"],
            vertical=True,
        )
        menus = Widget.Revealer(
            child=Widget.Box(
                child=[self.DateMenu(), self.BatteryMenu()],
                css_classes=["menu-main"],
                vertical=True,
                # spacing=10,
            ),
            reveal_child=self.visible["menus"].bind("value"),
            css_classes=["menu-revealer"],
            transition_type="slide_left",
        )
        main_tray = Widget.Box(
            child=[menus, chips],
            css_classes=["tray-main"],
        )
        revealer = Widget.Revealer(
            child=main_tray,
            reveal_child=self.visible["tray"].bind("value", lambda x: x),
            transition_type="slide_left",
            transition_duration=300,
            css_classes=["tray-revealer"],
        )
        Widget.Window(
            layer="overlay",
            namespace="Tray IGNIS",
            child=revealer,
            anchor=[
                "right",
                "top",
                "bottom",
            ],
        )


def main():
    bar = BAR()
    bar.tray()
    bar.tray_close_hitbox()
    bar.tray_open_hitbox()
