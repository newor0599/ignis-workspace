"""
Bluetooth Service

Requires [bluez]([bluetool](https://github.com/newor0599/bluetool)

Properties:
    - **devices** (``list[dict[str,str]]``, read-only): A list of nearby bluetooth devices
    - **connected_devices** (``list[dict[str,str]]``, read-only): A list of current connected devices
    - **paired_devices** (``list[dict[str,str]]``, read-only): A list of paired devices
"""

import time
import dbus
import dbus.mainloop.glib
from . import bluez_interactor
from ignis.base_service import BaseService
from ignis.utils import Utils
from ignis.exceptions import BluezNotFound, BluezInvalidGetCondition

class BluetoothService(BaseService):
    def __init__(self):
        super().__init__()
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._bus = dbus.SystemBus()
        self._scanning = False
        self._pairing = False
        self._connecting = False
        self._devices = []

    def get_pairable_devices(self) -> list[dict]:
        devices = self.get_available_devices()

        for key in self.get_paired_devices():
            devices.remove(key)

        return devices

    def available_devices(self) -> list[dict]:
        _available_devices = self.get("Available")
        return _available_devices

    def paired_devices(self) -> list[dict]:
        _paired_devices = self.get("Paired")
        return _paired_devices

    def connected_devices(self) -> list[dict]:
        _connected_devices = self.get("Connected")
        return _connected_devices

    def get(self, condition:str) -> list[dict]:
        devices = []
        conditions = ("available", "paired", "connected", "pairable")

        if condition not in conditions:
            BluezInvalidGetCondition()

        try:
            man = dbus.Interface(
                self._bus.get_object("org.bluez", "/"),
                "org.freedesktop.DBus.ObjectManager")
            objects = man.GetManagedObjects()

            for path, interfaces in objects.items():
                if "org.bluez.Device1" in interfaces:
                    dev = interfaces["org.bluez.Device1"]

                    if condition == "Available":
                        if "Address" not in dev:
                            continue

                        if "Name" not in dev:
                            dev["Name"] = "<unknown>"

                        device = {
                            "mac_address": dev["Address"],
                            "name": dev["Name"]
                        }

                        devices.append(device)
                    else:
                        props = dbus.Interface(
                            self._bus.get_object("org.bluez", path),
                            "org.freedesktop.DBus.Properties")

                        if props.Get("org.bluez.Device1", condition):
                            if "Address" not in dev:
                                continue

                            if "Name" not in dev:
                                dev["Name"] = "<unknown>"

                            device = {
                                "mac_address": dev["Address"],
                                "name": dev["Name"]
                            }

                            devices.append(device)
        except dbus.exceptions.DBusException as error:
            print(error)

        return devices

    def make_discoverable(self, value=True, timeout_sec=180):
        try:
            adapter = bluez_interactor.find_adapter()
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", adapter.object_path),
                "org.freedesktop.DBus.Properties")

            timeout_sec = int(timeout_sec)
            value = int(value)

            if int(props.Get(
                    "org.bluez.Adapter1", "DiscoverableTimeout")) != timeout_sec:
                props.Set(
                    "org.bluez.Adapter1", "DiscoverableTimeout",
                    dbus.UInt32(timeout_sec))

            if int(props.Get("org.bluez.Adapter1", "Discoverable")) != value:
                props.Set(
                    "org.bluez.Adapter1", "Discoverable", dbus.Boolean(value))
        except dbus.exceptions.DBusException as error:
            print(error)
            return False


        return True


    @Utils.run_in_thread #type: ignore
    def scan_devices(self, timeout_sec=10):
        if self._scanning:
            print("Bluetooth is already scanning")
            return
        self._scanning = True
        try:
            adapter = bluez_interactor.find_adapter()
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
        else:
            try:
                adapter.StartDiscovery()
                time.sleep(timeout_sec)
                adapter.StopDiscovery()
            except dbus.exceptions.DBusException as error:
                print(error)

        self._scanning = False
        self._devices = self.get_available_devices()


    def pair(self, address):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            if not props.Get("org.bluez.Device1", "Paired"):
                device.Pair()
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def connect(self, address):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            if not props.Get("org.bluez.Device1", "Connected"):
                device.Connect()
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def disconnect(self, address):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            if props.Get("org.bluez.Device1", "Connected"):
                device.Disconnect()
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def trust(self, address):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            if not props.Get("org.bluez.Device1", "Trusted"):
                props.Set("org.bluez.Device1", "Trusted", dbus.Boolean(1))
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def remove(self, address):
        try:
            adapter = bluez_interactor.find_adapter()
            dev = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            adapter.RemoveDevice(dev.object_path)
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def set_adapter_property(self, prop, value):
        try:
            adapter = bluez_interactor.find_adapter()
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", adapter.object_path),
                "org.freedesktop.DBus.Properties")

            if props.Get("org.bluez.Adapter1", prop) != value:
                props.Set("org.bluez.Adapter1", prop, value)
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def get_adapter_property(self, prop):
        try:
            adapter = bluez_interactor.find_adapter()
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return None

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", adapter.object_path),
                "org.freedesktop.DBus.Properties")

            return props.Get("org.bluez.Adapter1", prop)
        except dbus.exceptions.DBusException as error:
            print(error)
            return None

    def set_device_property(self, address, prop, value):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return False

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            if props.Get("org.bluez.Device1", prop) != value:
                props.Set("org.bluez.Device1", prop, value)
        except dbus.exceptions.DBusException as error:
            print(error)
            return False

        return True

    def get_device_property(self, address, prop):
        try:
            device = bluez_interactor.find_device(address)
        except (bluez_interactor.BluezUtilError,
                dbus.exceptions.DBusException) as error:
            print(error)
            return None

        try:
            props = dbus.Interface(
                self._bus.get_object("org.bluez", device.object_path),
                "org.freedesktop.DBus.Properties")

            return props.Get("org.bluez.Device1", prop)
        except dbus.exceptions.DBusException as error:
            print(error)
            return None
