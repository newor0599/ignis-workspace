from ignis.base_service import BaseService
from ignis.utils import Utils
from bleak import BleakScanner as scanner
from gi.repository import GObject  # type: ignore
import asyncio


class BluetoothService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self.scanned_devices:list[dict] = []
        self.raw_scanned_devices:list = []
        self._scanning = False

    async def scan_async(self) -> None:
        self._scanning = True
        self.notify('scanning')
        self.raw_scanned_devices = await scanner().discover()
        self._scanning = False

    @Utils.run_in_thread
    def scan(self)->list:
        asyncio.run(self.scan_async()) 
        devices = []
        for i in self.raw_scanned_devices:
            device = str(i).split(": ")
            devices.append({
                'name':device[1],
                'address':device[0]
                })
        self.scanned_devices = devices
        self.set_property("devices",self.scanned_devices)
        return devices

    @GObject.Property
    def devices(self)->list:
        return self.scanned_devices

    @GObject.Property
    def scanning(self)->bool:
        return self._scanning
