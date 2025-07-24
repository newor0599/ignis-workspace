from ignis.widgets import Widget
from . import logic


class BAR(logic.BAR):
    def DateChip(self):
        return Widget.Button(
            child=Widget.Box(
                child=[
                    Widget.Label(
                        label=self.time["month"].bind("value"),
                        css_classes=["date", "month", "chip"],
                    ),
                    Widget.Label(
                        label=self.time["day"].bind("value"),
                        css_classes=["date", "day", "chip"],
                    ),
                ],
                valign="center",
                vertical=True,
            ),
            css_classes=["tray", "chip", "date"],
            on_click=lambda x: (
                setattr(
                    self.visible["date_menu"],
                    "value",
                    not self.visible["date_menu"].value,
                ),
                self.menu_visibility(),
            ),
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
                            "percent", lambda x: str(int(x)) + "%"
                        )
                    ),
                ],
                vertical=True,
                valign="center",
            ),
            css_classes=["tray", "chip", "battery"],
            on_click=lambda x: (
                setattr(
                    self.visible["batt_menu"],
                    "value",
                    not self.visible["batt_menu"].value,
                ),
                self.menu_visibility(),
            ),
            tooltip_text=self.laptop_batt.bind_many(
                ["energy_rate", "percent", "time_remaining"],
                lambda x, y, z: f"{round(y)}%\n{round(x, 2)}w\n{z // 60}min",
            ),
        )

    def ClockChip(self):
        return Widget.Button(
            child=Widget.Label(
                label=self.time["time"].bind("value"),
                halign="center",
            ),
            css_classes=["tray", "chip", "clock"],
            on_click=lambda x: (
                setattr(
                    self.visible["date_menu"],
                    "value",
                    not self.visible["date_menu"].value,
                ),
                self.menu_visibility(),
            ),
        )

    def MixerChip(self):
        return Widget.Button(
            child=Widget.EventBox(
                child=[
                    Widget.Label(
                        label=" ",
                        halign="center",
                    ),
                    Widget.Label(
                        label=self.audio.speaker.bind(
                            "volume",
                            lambda x: str(x),
                        ),
                        halign="center",
                    ),
                ],
                halign="center",
                valign="center",
                vertical=True,
            ),
            css_classes=["tray", "chip"],
            on_click=lambda x: (
                setattr(
                    self.visible["mixer_menu"],
                    "value",
                    not self.visible["mixer_menu"].value,
                ),
                self.menu_visibility(),
            ),
        )
