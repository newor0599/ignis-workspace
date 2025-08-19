from ignis.services.audio import Stream
from ignis.services.bluetooth import BluetoothDevice
from ignis.widgets import Widget
from ignis.variable import Variable
from asyncio import create_task


class BaseMenu:
    def __init__(self, logic, title: str):
        self.logic = logic
        self.title = title
        self.content = [
            Widget.Label(label=self.title.title(), css_classes=["title"]),
        ]

    def menu(self) -> Widget.Revealer:
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=self.content,
                vertical=True,
                css_classes=["tray-menu", self.title.lower()],
            ),
            reveal_child=self.logic.visible[self.title.lower() + "_menu"].bind("value"),
            transition_type="slide_down",
        )
        return revealer


class DateMenu(BaseMenu):
    def __init__(self, logic):
        super().__init__(logic, "date")
        cal = Widget.Calendar()
        self.content.append(cal)


class BatteryMenu(BaseMenu):
    def __init__(self, logic):
        super().__init__(logic, "battery")
        percentage = Widget.Box(
            child=[
                Widget.Label(label=self.logic.battery_icon, css_classes=["icon"]),
                Widget.Scale(
                    value=self.logic.laptop_batt.bind("percent"),
                    css_classes=["scale"],
                    hexpand=True,
                    sensitive=False,
                ),
                Widget.Label(
                    label=self.logic.laptop_batt.bind(
                        "percent", lambda x: f"{int(x)}%"
                    ),
                    css_classes=["percent"],
                ),
            ],
            css_classes=["box"],
        )
        time = Widget.Box(
            child=[
                Widget.Label(label=" ", css_classes=["icon"]),
                Widget.Label(label=self.logic.battery_life.bind("value")),
            ],
            css_classes=["box"],
        )
        power = Widget.Box(
            child=[
                Widget.Label(label="󱐋 ", css_classes=["icon"]),
                Widget.Label(
                    label=self.logic.laptop_batt.bind(
                        "energy-rate", lambda x: str(round(x, 2)) + "w"
                    )
                ),
            ],
            css_classes=["box"],
        )
        self.content.append(percentage)
        self.content.append(time)
        self.content.append(power)


class MixerMenu(BaseMenu):
    def __init__(self, logic):
        super().__init__(logic, "mixer")
        speaker_list = Widget.DropDown(
            items=self.logic.sink_list.bind("value"),
            on_selected=lambda x, y: setattr(
                self.logic.audio, "speaker", self.logic.sinks[y]
            ),
        )
        mic_list = Widget.DropDown(
            items=self.logic.source_list.bind("value"),
            on_selected=lambda x, y: setattr(
                self.logic.audio, "microphone", self.logic.sources[y]
            ),
        )
        speaker_scale = self.audio_scale(self.logic.audio.speaker, self.logic.sink_icon)
        mic_scale = self.audio_scale(
            self.logic.audio.microphone, self.logic.source_icon
        )
        default_speaker = Widget.Box(
            child=[
                speaker_scale,
                speaker_list,
            ],
            vertical=True,
            css_classes=["box", "default"],
        )

        default_mic = Widget.Box(
            child=[
                mic_scale,
                mic_list,
            ],
            vertical=True,
            css_classes=["box", "default"],
        )

        apps_control = Widget.Box(
            css_classes=["apps-mixer", "box"],
            child=[Widget.Scroll(hexpand=True)],
        )

        setattr(
            apps_control.child[0],
            "child",
            Widget.Box(child=self.get_app_list(self.logic.audio.apps)),
        )

        self.logic.audio.connect(
            "notify::apps",
            lambda x, y: setattr(
                apps_control.child[0],
                "child",
                Widget.Box(child=self.get_app_list(x.apps)),
            ),
        )
        self.content += [default_speaker, default_mic, apps_control]

    def AppMixer(self, stream: Stream):
        return Widget.Box(
            vertical=True,
            vexpand=True,
            css_classes=["app-mixer"],
            tooltip_text=f"{stream.name}\n{stream.description}",
            child=[
                Widget.Scale(
                    vertical=True,
                    max=1,
                    step=0.05,
                    value=stream.bind("volume", lambda x: x / 100),
                    on_change=lambda x: setattr(stream, "volume", x.value * 100),
                    vexpand=True,
                ),
                Widget.Icon(
                    image=self.logic.get_app_icon(stream.name),
                    pixel_size=20,
                ),
            ],
        )

    def get_app_list(self, apps):
        if len(apps) <= 0:
            return [
                Widget.Label(
                    label=" No audio is currently playing",
                    valign="start",
                )
            ]
        return [self.AppMixer(i) for i in apps]

    def audio_scale(self, audio: Stream, icon: Variable):
        return Widget.Box(
            child=[
                Widget.Label(label=icon.bind("value"), css_classes=["icon"]),
                Widget.Scale(
                    max=100,
                    step=5,
                    value=audio.bind(
                        "volume",
                        lambda x: x,
                    ),
                    on_change=lambda x: setattr(audio, "volume", x.value),
                    hexpand=True,
                ),
            ],
        )


class NetworkMenu(BaseMenu):
    def __init__(self, logic):
        super().__init__(logic, "network")

        wifi_list = Variable(value=[])
        setattr(wifi_list, "value", self.update_wifi())
        self.logic.wifi_device.connect(
            "new_access_point",
            lambda x, y: setattr(wifi_list, "value", self.update_wifi()),
        )

        scroll = Widget.Scroll(
            child=Widget.Box(child=wifi_list.bind("value"), vertical=True),
            style="min-height:20rem;",
        )

        scan_btn = Widget.Button(
            label="Scan",
            on_click=lambda x: create_task(self.logic.wifi_device.scan()),
        )

        self.content.append(scroll)
        self.content.append(scan_btn)

    def WifiPoint(self, wifi_ap):
        # Widgets
        expand = Variable(
            value={
                "entry": False,
                "action": False,
            }
        )
        connection_label = Variable(value="Disconnect")
        connection_on_click = Variable()
        entry = Widget.Revealer(
            child=Widget.Entry(
                visibility=False,
                placeholder_text="Enter password",
                on_accept=lambda x: create_task(wifi_ap.connect_to(x.text)),
                css_classes=["wifi-ap"],
            ),
            reveal_child=expand.bind("value", lambda x: x["entry"]),
        )
        ssid = Widget.Label(
            label=wifi_ap.ssid,
            valign="center",
            vexpand=True,
        )
        arrow = Widget.Arrow(
            pixel_size=20,
            rotated=expand.bind("value", lambda x: x["entry"] or x["action"]),
            degree=90,
            valign="center",
            vexpand=True,
        )
        connection = Widget.Button(
            label=connection_label.bind("value"),
            on_click=connection_on_click.bind("value"),
        )
        header = Widget.EventBox(
            child=[
                ssid,
                arrow,
            ],
            on_click=lambda x: (
                expand.value.update({"action": not expand.value["action"]})
                if wifi_ap.is_connected
                else expand.value.update({"entry": not expand.value["entry"]}),
                setattr(expand, "value", expand.value),
            ),
        )
        actions = Widget.Revealer(
            child=Widget.Box(
                child=[
                    connection,
                ],
                css_classes=["wifi-ap", "action"],
            ),
            reveal_child=expand.bind("value", lambda x: x["action"]),
        )

        # Logic
        wifi_ap.connect(
            "notify::is_connected",
            lambda x, y: (
                setattr(
                    connection_label,
                    "value",
                    "Disconnect" if x.is_connected else "Connect",
                ),
                setattr(
                    connection_on_click,
                    "value",
                    lambda x: create_task(wifi_ap.disconnect_from())
                    if x.is_connected
                    else lambda x: create_task(wifi_ap.connect_to()),
                ),
                expand.value.update({"entry": False}) if wifi_ap.is_connected else None,
                setattr(expand, "value", expand.value),
            ),
        )

        return Widget.Box(
            child=[header, entry, actions],
            vertical=True,
            css_classes=["wifi-ap", "main"],
        )

    def update_wifi(self):
        wifi_list = []
        for i in self.logic.wifi_device.access_points:
            if i.ssid is not None:
                wifi_list.append(self.WifiPoint(i))
        return wifi_list


class BluetoothMenu(BaseMenu):
    def __init__(self, logic):
        super().__init__(logic, "bluetooth")
        device_list = Variable(value=[])
        scroll = Widget.Scroll(
            child=Widget.Box(child=device_list.bind("value"), vertical=True),
            style="min-height:20rem;",
        )
        scan_button = Widget.Button(
            label="Scan",
            on_click=lambda x: setattr(self.logic.bt, "setup_mode", True),
        )
        self.logic.bt.connect(
            "notify::devices",
            lambda x, y: setattr(device_list, "value", self.update_devices()),
        )
        self.content.append(scroll)
        self.content.append(scan_button)

    def device(self, device: BluetoothDevice):
        icon = Variable(value="")
        indicator = Widget.Label(
            css_classes=["ind"],
            label=icon.bind("value"),
            halign="end",
            hexpand=True,
            valign="center",
        )
        main = Widget.EventBox(
            child=[
                Widget.Label(
                    label=device.alias,
                    halign="start",
                ),
                indicator,
            ],
            css_classes=["bt", "device"],
            on_click=device.bind(
                "connected", lambda x: self.logic.get_bt_device_action(device)
            ),
        )
        icon.set_value(self.logic.get_bt_device_icon(device))
        device.connect(
            "notify::connected",
            lambda x, y: setattr(icon, "value", self.logic.get_bt_device_icon(device)),
        )
        return main

    def update_devices(self):
        return [self.device(i) for i in self.logic.bt.devices]
