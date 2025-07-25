from ignis.widgets import Widget
from . import logic


class BAR(logic.BAR):
    def BatteryMenu(self):
        title = Widget.Label(
            label="Battery",
            css_classes=["title"],
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
            ],
            css_classes=["box"],
        )
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=[title, percentage, time, power],
                vertical=True,
                css_classes=["batt"],
            ),
            reveal_child=self.visible["batt_menu"].bind("value"),
            css_classes=["tray-menu", "batt"],
        )
        return revealer

    def DateMenu(self):
        title = Widget.Label(
            label="Date",
            css_classes=["title"],
            # halign="center",
        )
        cal = Widget.Calendar()
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=[title, cal],
                css_classes=["date"],
                vexpand=False,
                vertical=True,
            ),
            reveal_child=self.visible["date_menu"].bind("value"),
            transition_type="slide_down",
            vexpand=False,
            valign="start",
            css_classes=["tray-menu", "date"],
        )
        return revealer

    def MixerMenu(self):
        title = Widget.Label(label="Mixer", css_classes=["title"])
        speaker_list = Widget.DropDown(
            items=self.speaker_list.bind("value"),
            on_selected=lambda x, y: self.change_speaker(y),
        )
        mic_list = Widget.DropDown(
            items=self.mic_list.bind("value"),
            on_selected=lambda x, y: self.change_mic(y),
        )
        default_speaker = Widget.Box(
            child=[
                Widget.Box(
                    child=[
                        Widget.Label(label="󰓃", css_classes=["icon"]),
                        Widget.Scale(
                            max=1,
                            step=0.05,
                            value=self.audio.speaker.bind(
                                "volume",
                                lambda x: x / 100,
                            ),
                            on_change=lambda x: setattr(
                                self.audio.speaker, "volume", x.value * 100
                            ),
                            hexpand=True,
                        ),
                    ],
                ),
                speaker_list,
            ],
            vertical=True,
            css_classes=["box"],
        )

        default_mic = Widget.Box(
            child=[
                Widget.Box(
                    child=[
                        Widget.Label(label="", css_classes=["icon"]),
                        Widget.Scale(
                            max=1,
                            step=0.05,
                            value=self.audio.microphone.bind(
                                "volume",
                                lambda x: x / 100,
                            ),
                            on_change=lambda x: setattr(
                                self.audio.microphone, "volume", x.value * 100
                            ),
                            hexpand=True,
                        ),
                    ],
                ),
                mic_list,
            ],
            vertical=True,
            css_classes=["box"],
        )

        grouper = Widget.Box(
            child=[
                title,
                default_speaker,
                default_mic,
            ],
            vertical=True,
        )
        revealer = Widget.Revealer(
            child=grouper,
            reveal_child=self.visible["mixer_menu"].bind("value"),
            transition_type="slide_down",
            css_classes=["tray-menu", "mixer"],
        )
        return revealer
