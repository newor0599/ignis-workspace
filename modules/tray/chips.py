from ignis.widgets import Widget
from ignis.utils import Utils
from asyncio import create_task


class BaseChip(Widget.Button):
    def __init__(self, logic, name: str, content: list[Widget]):
        css = ["tray", "chip", name]
        if "icon" not in content[0].css_classes:
            content[0].css_classes += ["icon"]
        super().__init__(
            child=Widget.Box(
                child=content,
                valign="center",
                vertical=True,
            ),
            css_classes=logic.visible[f"{name}_menu"].bind(
                "value", lambda x: css + ["active"] if x else css
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


def DateChip(self):
    return BaseChip(
        self,
        "date",
        [
            Widget.Label(
                label=self.time["month"].bind("value"),
                css_classes=["date", "month", "chip"],
            ),
            Widget.Label(
                label=self.time["day"].bind("value"),
                css_classes=["date", "day", "chip"],
            ),
        ],
    )


def BatteryChip(self):
    chip = BaseChip(
        self,
        "battery",
        [
            Widget.Label(
                label=self.battery_icon,
            ),
            Widget.Label(label=self.laptop_batt.bind("percent", lambda x: str(int(x)))),
        ],
    )

    chip.tooltip_text = self.laptop_batt.bind_many(
        ["energy_rate", "percent", "time_remaining"],
        lambda x,
        y,
        z: f"{round(y)}%\n{round(x, 2)}w\n{self.calc_batt_life().replace(' hour', 'h').replace(' min', 'm').replace(' left', '')}",
    )
    return chip


def ClockChip(self):
    return BaseChip(
        self,
        "date",
        [Widget.Label(label=self.time["time"].bind("value"), halign="center")],
    )


def MixerChip(self):
    return BaseChip(
        self,
        "mixer",
        [Widget.Label(label=" ", halign="center")],
    )


def NetChip(self):
    return BaseChip(
        self,
        "network",
        [
            Widget.Label(
                label=self.network_icon.bind("value"),
            ),
            Widget.Label(label=self.wifi_device.ap.bind("strength", lambda x: str(x))),
        ],
    )


def BluetoothChip(self):
    return BaseChip(
        self,
        "bluetooth",
        [
            Widget.Label(
                label="󰂯",
            ),
        ],
    )


def WallpaperChip(self):
    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label=" ",
                    css_classes=["icon"],
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
        css = ["workspace-dot"]
        return Widget.EventBox(
            css_classes=self.mangowc["focus tag"].bind(
                "value", lambda x: css + ["active"] if x == number else css
            ),
            hexpand=False,
            halign="center",
            on_click=lambda x: self.set_mango_tag(number),
        )

    return Widget.Box(
        child=[workspace_dot(i + 1) for i in range(9)],
        vertical=True,
        css_classes=["workspace", "tray", "chip"],
        # halign="center",
    )
