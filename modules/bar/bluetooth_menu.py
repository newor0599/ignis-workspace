from ignis.widgets import Widget
from bluetooth import BluetoothService




class BluetoothMenu(Widget.Box):
    def __init__(self):
        self.indicator = Widget.Box(
                css_classes = ['bt','scanning-indicator'],
                child = [
                    Widget.Label(label = "Scanning for bluetooth devices"),
                    ]
                )
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
                        on_click = lambda x:self._scan(),
                        child = Widget.Label(label = "Scan"),
                        css_classes = ['bt','scan-button'],
                        )
                    ]
                )

    def device_box(self,device) -> Widget.EventBox:
        name = device['name'].decode('utf-8')
        if device['name'] == b'<unknown>':
            name = device['mac_address'].decode('utf-8')

        def button_on_click(device):
            if not device['connected']:
                self.bt.connect_device(device)
            else:
                self.bt.disconnect_device(device)


        box = Widget.EventBox(
                on_click = lambda x,y=device: button_on_click(y),
            on_hover = lambda x: box.add_css_class("hover"),
            on_hover_lost = lambda x:box.remove_css_class('hover'),
            css_classes = ['bt','device','connected' if device['connected'] else 'disconnected', 'paired' if device['paired'] else 'unpaired'],
            child = [Widget.Label(label = name)],
        )
        return box

    def _scan(self):
        print("Scanning")
        self.scanning_indicator()
        self.bt.scan_devices()

    def scanning_indicator(self):
        devices = self.bluetooth_menu.child
        print(devices)
        devices.insert(0,self.indicator)
        self.bluetooth_menu.set_child(devices)

    def update_menu(self):
        device_selections = []
        for device in self.bt.devices:
            device_selections.append(self.device_box(device))

        self.bluetooth_menu.set_child(device_selections)
