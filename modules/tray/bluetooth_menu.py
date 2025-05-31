from ignis.widgets import Widget
from ignis.services.bluetooth import BluetoothService
from ignis.utils import Utils


class BluetoothMenu(Widget.Box):
    def __init__(self):
        self.indicator = Widget.Box(
            css_classes=["bt", "scanning-indicator"],
            child=[
                Widget.Label(label="Scanning for bluetooth devices"),
            ],
        )
        self.bluetooth_menu = Widget.Box(vertical=True)
        self.hide_nameless_device = True
        self.bt = BluetoothService()
        self.bt.connect("notify::devices", lambda x, y: self.update_menu())
        self.bluetooth_scroll = Widget.Scroll(
            css_classes=["bt", "main"],
            child=self.bluetooth_menu,
            hexpand=True,
            vexpand=True,
        )

        super().__init__(
            vertical=True,
            css_classes=["bt", "window"],
            hexpand=True,
            vexpand=True,
            child=[
                self.bluetooth_scroll,
                Widget.Button(
                    on_click=lambda x: self._scan(),
                    child=Widget.Label(label="Scan"),
                    css_classes=["bt", "scan-button"],
                ),
            ],
        )

    def device_state(self, device) -> str:
        if device.connected:
            return "  "
        if device.paired:
            return "󰀚  "
        return "  "

    def device_box(self, device) -> Widget.EventBox:
        name = device.name
        stateIcon = Widget.Label(
            label=self.device_state(device),
            hexpand=True,
            halign="end",
        )
        self.bt.connect(
            "notify::devices",
            lambda x, y: stateIcon.set_label(self.device_state(device)),
        )

        @Utils.run_in_thread
        def button_on_click(device):
            if not device.connected:
                device.connect_to()
            else:
                device.disconnect_from()

        box = Widget.EventBox(
            on_click=lambda x, y, z=device: button_on_click(z),
            on_hover=lambda x: box.add_css_class("hover"),
            on_hover_lost=lambda x: box.remove_css_class("hover"),
            css_classes=[
                "bt",
                "device",
                "connected" if device.connected else "disconnected",
                "paired" if device.paired else "unpaired",
            ],
            child=[Widget.Label(label=name), stateIcon],
        )
        return box

    def _scan(self):
        self.bt.set_powered(True)
        self.bt.set_setup_mode(True)
        Utils.Timeout(ms=10000, target=lambda: self.bt.set_setup_mode(False))

    def update_menu(self):
        device_selections = []
        for device in self.bt.devices:
            if device.name is not None:
                device_selections.append(self.device_box(device))

        self.bluetooth_menu.set_child(device_selections)
