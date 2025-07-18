from ignis.widgets import Widget
from . import logic


class BAR(logic.BAR):
    # Hitbox
    def tray_open_hitbox(self):
        Widget.Window(
            namespace="Tray Hitbox IGNIS",
            child=Widget.EventBox(
                css_classes=["tray", "hitbox"],
                on_hover=lambda x: setattr(self.visible, "value", True),
            ),
            anchor=["top", "right"],
        )

    def tray_close_hitbox(self):
        Widget.Window(
            namespace="Tray Close Hitbox IGNIS",
            child=Widget.EventBox(
                on_click=lambda x: setattr(self.visible, "value", False)
            ),
            anchor=["top", "bottom", "left", "right"],
            visible=self.visible.bind("value", lambda x: x),
        )

    def ClockChip(self):
        return Widget.Button(
            child=Widget.Label(
                label=self.time.bind("value", lambda x: x),
                halign="center",
            ),
            css_classes=["tray", "chip", "clock"],
        )

    def BatteryChip(self):
        return Widget.Button(
            child=Widget.Box(
                child=[
                    Widget.Label(
                        label=self.battery_icon,
                    ),
                    Widget.Label(
                        label=self.laptop_batt.bind(
                            "energy_rate", lambda x: str(int(x)) + "w"
                        )
                    ),
                ],
                vertical=True,
                valign="center",
            ),
            css_classes=["tray", "chip", "battery"],
            tooltip_text=self.laptop_batt.bind_many(
                ["energy_rate", "percent", "time_remaining"],
                lambda x, y, z: f"{round(y)}%\n{round(x, 2)}w\n{z // 60}min",
            ),
        )

    def DateChip(self):
        return Widget.Button(
            child=Widget.Box(
                child=[
                    Widget.Label(
                        label=self.month.bind("value", lambda x: x),
                        css_classes=["date", "month", "chip"],
                    ),
                    Widget.Label(
                        label=self.day.bind("value", lambda x: x),
                        css_classes=["date", "day", "chip"],
                    ),
                ],
                valign="center",
                vertical=True,
            ),
            css_classes=["tray", "chip", "date"],
        )

    # Hitbox
    def tray(self):
        main_tray = Widget.Box(
            child=[self.ClockChip(), self.DateChip(), self.BatteryChip()],
            halign="end",
            vexpand=True,
            css_classes=["tray", "main"],
            vertical=True,
        )
        revealer = Widget.Revealer(
            child=main_tray,
            reveal_child=self.visible.bind("value", lambda x: x),
            transition_type="slide_left",
            transition_duration=300,
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
