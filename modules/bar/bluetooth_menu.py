from ignis.widgets import Widget
from bluetooth import BluetoothService


class BluetoothMenu(Widget.Box):
    def __init__(self):
        self.bluetooth_menu = Widget.Box(
                vertical = True
                )
        self.bt = BluetoothService()
        self.bt.connect("notify::devices",lambda x,y: self.update_menu())
        self.bluetooth_scroll = Widget.Scroll(
                                    css_classes = ['bt','main'],
                                    child = self.bluetooth_menu,
                                )

        super().__init__(
                vertical = True,
                css_classes = ['bt','window'],
                child = [
                    self.bluetooth_scroll,
                    Widget.Button(
                        on_click = lambda x:self.bt.scan_devices(),
                        child = Widget.Label(label = "Scan"),
                        css_classes = ['bt','scan-button'],
                        )
                    ]
                )

    def update_menu(self):
        print("Updating bluetooth menu")
        device_selections = []
        for i in self.bt.devices:
            name = i['name'].decode('utf-8')
            if i['name'] == b'<unknown>':
                name = i['mac_address'].decode('utf-8')

            device_selections.append(
                    Widget.EventBox(
                        on_click = lambda x,device=i:self.bt.connect_device(device),
                        css_classes = ['bt','device','connected' if i['connected'] else 'disconnected', 'paired' if i['paired'] else 'unpaired'],
                        child = [Widget.Label(label = name)],
                        )
                    )

        self.bluetooth_menu.set_child(device_selections)
        print("Update complete")
