from ignis.services.upower import UPowerService
from ignis.utils import Utils
import asyncio


class SYSTEM_NOTIF:
    def __init__(self):
        self.service_inits()
        self.laptop_battery = self.upower.display_device
        self.low_battery_notified = False
        self.charging_notified = False
        self.laptop_battery.connect(
            "notify::percent", lambda x, y: self.low_battery_notify()
        )
        self.laptop_battery.connect(
            "notify::charging", lambda x, y: self.charging_notify()
        )
        self.low_battery_notify()

    def service_inits(self):
        self.upower = UPowerService.get_default()

    def notify(self, text: str, summary: str = "system"):
        asyncio.create_task(
            Utils.exec_sh_async(f"notify-send -a System '{summary}' '{text}'")
        )

    def low_battery_notify(self):
        if self.laptop_battery.charging:
            return
        if self.laptop_battery.percent <= 5:
            self.notify(
                f"Battery is at {int(self.laptop_battery.percent)}%, charge now!"
            )
            return
        if self.laptop_battery.percent <= 15 and not self.low_battery_notified:
            self.notify(f"Battery is at {int(self.laptop_battery.percent)}%")
            self.low_battery_notified = True

    def charging_notify(self):
        if self.laptop_battery.charging and not self.charging_notified:
            self.notify("Battery is being charged!")
            self.charging_notified = True
            return
        if not self.laptop_battery.charging and self.charging_notified:
            self.charging_notified = False
