from ignis.widgets import Widget
from ignis.utils import Utils
from asyncio import create_task


def BaseChip(name: str, content: list, logic):
    name = name.lower()
    css = ["tray", "chip", name]
    btn = Widget.Button(
        child=Widget.Box(
            child=content,
            vertical=True,
            valign="center",
        ),
        css_classes=logic.visible[f"{name}_menu"].bind(
            "value",
            lambda x: css + ["active"] if x else css,
        ),
        on_click=lambda x: (
            setattr(
                logic.visible[f"{name}_menu"],
                "value",
                not logic.visible[f"{name}_menu"].value,
            ),
            logic.menu_visibility(),
        ),
    )
    return btn


def DateChip(logic):
    return BaseChip(
        "date",
        [
            Widget.Label(
                label=logic.time["month"].bind("value"),
                css_classes=["date", "month", "chip"],
            ),
            Widget.Label(
                label=logic.time["day"].bind("value"),
                css_classes=["date", "day", "chip"],
            ),
        ],
        logic,
    )


def BatteryChip(self):
    return BaseChip(
        "battery",
        [
            Widget.Label(label=self.battery_icon),
            Widget.Label(label=self.laptop_batt.bind("percent", lambda x: str(int(x)))),
        ],
        self,
    )


def ClockChip(self):
    return BaseChip(
        "date",
        [
            Widget.Label(
                label=self.time["time"].bind("value"),
                halign="center",
            )
        ],
        self,
    )


def MixerChip(self):
    return BaseChip(
        "mixer",
        [
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
        self,
    )


def NetChip(self):
    return BaseChip(
        "network",
        [
            Widget.Label(label=self.network_icon.bind("value")),
            Widget.Label(
                label=self.wifi_device.ap.bind(
                    "strength",
                    lambda x: str(x),
                )
            ),
        ],
        self,
    )


def BluetoothChip(self):
    return BaseChip(
        "bluetooth",
        [
            Widget.Label(label="󰂯"),
        ],
        self,
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


def WorkspaceChip(self):
    def workspace_dot(number: int):
        return Widget.EventBox(
            css_classes=self.mangowc["focus workspace"].bind(
                "value",
                lambda x: ["workspace-dot", "active"]
                if x == number
                else ["workspace-dot"],
            ),
            on_click=lambda x: self.set_workspace(number),
            on_scroll_up=lambda x: self.set_workspace(
                self.mangowc["focus workspace"].value + 1
            ),
            on_scroll_down=lambda x: self.set_workspace(
                self.mangowc["focus workspace"].value - 1
            ),
        )

    return Widget.EventBox(
        child=[workspace_dot(i + 1) for i in range(self.mangowc["workspace size"])],
        spacing=10,
        vertical=True,
        css_classes=["tray", "chip", "workspace"],
        on_scroll_up=lambda x: self.set_workspace(
            self.mangowc["focus workspace"].value + 1
        ),
        on_scroll_down=lambda x: self.set_workspace(
            self.mangowc["focus workspace"].value - 1
        ),
    )


def AboutChip(self):
    return BaseChip("about", [Widget.Button(label="󰋼 ")], self)
