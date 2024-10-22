from ignis.widgets import Widget
from bluetooth import BluetoothService
bt = BluetoothService()

bluetooth_menu = Widget.ListBox(
        css_classes = ['bt','main'],
        )

bt.connect("notify::devices",lambda x,y: update_menu())
def update_menu():
    print("Updating bluetooth menu")
    device_selections = []
    for i in bt.devices:
        address = i['mac_address'].decode('utf-8')
        name = i['name'].decode('utf-8')
        if i['name'] == b'<unknown>':
            name = i['mac_address'].decode('utf-8')

        device_selections.append(
                Widget.ListBoxRow(
                    on_activate = lambda x,device=i:bt.connect_device(device),
                    css_classes = ['bt','device','connected' if i['connected'] else 'disconnected', 'paired' if i['paired'] else 'unpaired'],
                    child = Widget.Label(label = name)
                    )
                )
    bluetooth_menu.set_rows(device_selections)
    print("Update complete")

Widget.Window(
        namespace="Bluetooth Menu",
        anchor = ['right','top','bottom'],
        layer = 'background',
        exclusivity='normal',
        child = Widget.Box(
            vertical = True,
            css_classes = ['bt','window'],
            child = [
                bluetooth_menu,
                Widget.Button(
                    on_click = lambda x:bt.scan_devices(),
                    child = Widget.Label(label = "Scan"),
                    css_classes = ['bt','scan-button'],
                    )
                ],
            )        
        )
