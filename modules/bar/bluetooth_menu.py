from ignis.app import IgnisApp
from ignis.widgets import Widget
from bluetooth import BluetoothService
bt = BluetoothService()
bt.scan()
bt.connect("notify::devices",lambda x,y: update_menu())


bluetooth_menu = Widget.ListBox(
        css_classes = ['bt','main'],
        )
def update_menu():
    device_selections = []
    for i in bt.devices:
        device_selections.append(
                Widget.ListBoxRow(
                    on_activate = lambda x,y=i:print(f"Connecting to Device {y['name']} Address {y['address']}"),
                    css_classes = ['bt','device'],
                    child = Widget.Label(label = i['name'])
                    )
                )
    bluetooth_menu.set_rows(device_selections)

Widget.Window(
        namespace="Bluetooth Menu",
        # anchor = ['right'],
        layer = 'background',
        exclusivity='normal',
        css_classes = ['bt','window'],
        # child = bluetooth_menu,
        child = Widget.Box(
            css_classes = ['bt','test'],
            child = [Widget.Label(label = "Hello")],
            )
        )
