from ignis.widgets import Widget
from ignis.utils import Utils
from asyncio import create_task


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
        css_classes=self.visible["date_menu"].bind(
            "value",
            lambda x: ["tray", "chip", "date", "active"]
            if x
            else ["tray", "chip", "date"],
        ),
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
                    label=self.laptop_batt.bind("percent", lambda x: str(int(x)))
                ),
            ],
            vertical=True,
            valign="center",
        ),
        css_classes=self.visible["battery_menu"].bind(
            "value",
            lambda x: ["tray", "chip", "battery", "active"]
            if x
            else ["tray", "chip", "battery"],
        ),
        on_click=lambda x: (
            setattr(
                self.visible["battery_menu"],
                "value",
                not self.visible["battery_menu"].value,
            ),
            self.menu_visibility(),
        ),
        tooltip_text=self.laptop_batt.bind_many(
            ["energy_rate", "percent", "time_remaining"],
            lambda x,
            y,
            z: f"{round(y)}%\n{round(x, 2)}w\n{self.calc_batt_life().replace(' hour', 'h').replace(' min', 'm').replace(' left', '')}",
        ),
    )


def ClockChip(self):
    classes = ["tray", "chip", "clock"]
    main = Widget.Button(
        child=Widget.Label(
            label=self.time["time"].bind("value"),
            halign="center",
        ),
        css_classes=self.visible["date_menu"].bind(
            "value",
            lambda x: classes + ["active"] if x else classes,
        ),
        on_click=lambda x: (
            setattr(
                self.visible["date_menu"],
                "value",
                not self.visible["date_menu"].value,
            ),
            self.menu_visibility(),
        ),
    )
    return main


def MixerChip(self):
    classes = ["tray", "chip"]
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
        css_classes=self.visible["mixer_menu"].bind(
            "value", lambda x: classes + ["active"] if x else classes
        ),
        on_click=lambda x: (
            setattr(
                self.visible["mixer_menu"],
                "value",
                not self.visible["mixer_menu"].value,
            ),
            self.menu_visibility(),
        ),
    )


def NetChip(self):
    classes = ["tray", "chip", "network"]
    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label=self.network_icon.bind("value"),
                ),
                Widget.Label(
                    label=self.wifi_device.ap.bind("strength", lambda x: str(x))
                ),
            ],
            vertical=True,
            valign="center",
        ),
        css_classes=self.visible["network_menu"].bind(
            "value", lambda x: classes + ["active"] if x else classes
        ),
        on_click=lambda x: (
            setattr(
                self.visible["network_menu"],
                "value",
                not self.visible["network_menu"].value,
            ),
            self.menu_visibility(),
        ),
    )


def BluetoothChip(self):
    classes = ["tray", "chip", "bluetooth"]
    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label="󰂯",
                ),
                Widget.Label(
                    label=self.bt_connected_length.bind("value"),
                ),
            ],
            vertical=True,
            valign="center",
        ),
        css_classes=self.visible["bluetooth_menu"].bind(
            "value", lambda x: classes + ["active"] if x else classes
        ),
        on_click=lambda x: (
            setattr(
                self.visible["bluetooth_menu"],
                "value",
                not self.visible["bluetooth_menu"].value,
            ),
            self.menu_visibility(),
        ),
    )


def WallpaperChip(self):
    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label=" ",
                ),
            ],
            vertical=True,
            valign="center",
        ),
        css_classes=["tray", "chip"],
        on_click=lambda x: create_task(
            Utils.exec_sh_async("~/.config/mango/scripts/wallpaper-picker")
        ),
    )
