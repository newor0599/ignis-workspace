from ignis.base_service import BaseService
from ignis.utils import Utils
from gi.repository import GObject  # type: ignore
from bluetool import Bluetooth

"""
Bluetooth Service

Requires [bluetool](https://github.com/newor0599/bluetool)

Properties:
    - **devices** (``list[dict[str,str]]``, read-only): A list of nearby bluetooth devices
    - **connected_devices** (``list[dict[str,str]]``, read-only): A list of current connected devices
    - **paired_devices** (``list[dict[str,str]]``, read-only): A list of paired devices
"""


class BluetoothService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self.bt = Bluetooth()
        self._devices = []
        self._scanning = False
        self._old_devices = []
    
    @Utils.run_in_thread #type: ignore
    def scan_devices(self):
        if self._scanning:
            return
        self._scanning = True
        self.bt.scan(2)
        self._devices = self.bt.get_available_devices()

        for i in range(len(self._devices)):
            self._devices[i].update({"connected":False,"paired":False})

        for connected in self.bt.get_connected_devices():
            for i,device in enumerate(self._devices):
                if device['mac_address'] == connected["mac_address"]:
                    self._devices[i].update({"connected":True})

        for paired in self.bt.get_paired_devices():
            for i,device in enumerate(self._devices):
                if device['mac_address'] == paired["mac_address"]:
                    self._devices[i].update({"paired":True})
        self._scanning = False
        self.notify("devices")

    def connect_device(self,device:dict) -> None:
        for connected in self.bt.get_connected_devices():
            if connected['mac_address'] == device['mac_address']:
                print("Device already connected")
                return
        print("Connecting to",device['name'])
        address = device['mac_address'].decode("utf-8")
        if not device['paired']:
            print("Device is not paired, trusting and pairing")
            self.bt.trust(address)
            self.bt.pair(address)
            print(self.bt.trust(address))
            print(self.bt.pair(address))
        print("Connecting now")
        self.bt.connect(address)
        print("Device Connected")
        device.update({'connected':True})
        print(self.bt.get_available_devices())
        if self._old_devices != self.bt.get_available_devices():
            self._old_devices = self.bt.get_available_devices()
            self.notify("devices")
        # return device

    def disconnect_device(self,device:dict) -> None:
        self.bt.disconnect(device['mac_address'].decode("utf-8"))
        self.notify("devices")

    @GObject.Property
    def devices(self) -> list:
        devices_sort = sorted(self._devices,key=lambda x:x['paired'],reverse=True)
        devices_sort = sorted(devices_sort,key=lambda x:x['connected'],reverse=True)
        return devices_sort

    @GObject.Property
    def connected_devices(self) -> list[dict]:
        return self.bt.get_connected_devices()

    @GObject.Property
    def paired_devices(self) -> list[dict]:
        return self.bt.get_paired_devices()
