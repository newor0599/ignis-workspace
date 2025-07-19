from ignis.widgets import Widget
from . import logic


class BAR(logic.BAR):
    def BatteryMenu(self):
        title = Widget.Label(
            label="Battery",
            css_classes=["batt", "menu", "title"],
        )
        percentage = Widget.Box(
            child=[
                Widget.Label(
                    label=self.battery_icon,
                    css_classes=["icon"],
                ),
                Widget.Scale(
                    value=self.laptop_batt.bind("percent"),
                    css_classes=["scale"],
                    hexpand=True,
                    sensitive=False,
                ),
                Widget.Label(
                    label=self.laptop_batt.bind("percent", lambda x: f"{str(int(x))}%"),
                    css_classes=["percent"],
                ),
            ],
            css_classes=["box"],
        )
        time = Widget.Box(
            child=[
                Widget.Label(label=" ", css_classes=["icon"]),
                Widget.Label(label=self.battery_life.bind("value")),
            ],
            css_classes=["box"],
        )
        source = Widget.Box(
            child=[
                Widget.Label(label="󱄉 ", css_classes=["icon"]),
                # Widget.Label(label=self.laptop_batt.bind())
            ]
        )
        power = Widget.Box(
            child=[
                Widget.Label(label="󱐋", css_classes=["icon"]),
                Widget.Label(
                    label=self.laptop_batt.bind("energy-rate", lambda x: str(x) + "w")
                ),
            ]
        )
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=[title, percentage, time, power],
                vertical=True,
                css_classes=["menu", "batt", "main"],
                spacing=10,
            ),
            reveal_child=self.visible["batt_menu"].bind("value"),
            css_classes=["menu", "revealer"],
        )
        return revealer

    def DateMenu(self):
        title = Widget.Label(
            label="Date",
            css_classes=["date", "menu", "title"],
            # halign="center",
        )
        cal = Widget.Calendar()
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=[title, cal],
                css_classes=["date", "menu", "main"],
                vexpand=False,
                vertical=True,
                spacing=10,
            ),
            reveal_child=self.visible["date_menu"].bind("value"),
            transition_type="slide_down",
            vexpand=False,
            valign="start",
            css_classes=["menu", "revealer"],
        )
        return revealer
