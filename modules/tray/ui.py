from ignis.widgets import Widget
from . import chips
from . import menus
from . import hitboxes
from . import logic


class BAR(logic.BAR):
    def tray(self):
        chip_list = Widget.Box(
            child=[
                chips.ClockChip(self),
                chips.DateChip(self),
                chips.BatteryChip(self),
                chips.MixerChip(self),
            ],
            vexpand=True,
            css_classes=["chip-main"],
            vertical=True,
        )
        menu_list = Widget.Revealer(
            child=Widget.Scroll(
                child=Widget.Box(
                    child=[
                        menus.DateMenu(self),
                        menus.BatteryMenu(self),
                        menus.MixerMenu(self),
                    ],
                    vertical=True,
                    hexpand=True,
                ),
                css_classes=["menu-main"],
                vexpand=True,
                hexpand=True,
                style="min-width:20rem;",
            ),
            reveal_child=self.visible["menus"].bind("value"),
            css_classes=["menu-revealer"],
            transition_type="slide_left",
        )
        main_tray = Widget.Box(
            child=[menu_list, chip_list],
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
    hitboxes.tray_close_hitbox(bar)
    hitboxes.tray_open_hitbox(bar)
