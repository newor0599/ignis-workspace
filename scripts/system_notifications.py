from ignis.services.upower import UPowerService
from ignis.utils import Utils
import asyncio


class SYSTEM_NOTIF:
    def __init__(self):
        self.service_inits()
        self.laptop_battery = self.upower.display_device
        self.notified = {
            "low bat": False,
            "charging": False,
            "charged": False,
        }
        self.battery_state = {
            "max": 90,
            "low": 15,
            "lower": 5,
        }
        self.laptop_battery.connect(
            "notify::percent",
            lambda x, y: (
                self.low_battery_notify(),
                self.charged_notify(),
            ),
        )
        self.laptop_battery.connect(
            "notify::charging", lambda x, y: self.charging_notify()
        )
        self.low_battery_notify()

    def service_inits(self):
        self.upower = UPowerService.get_default()

    def notify(self, text: str, summary: str = "system", sound: bool = False):
        asyncio.create_task(
            Utils.exec_sh_async(f"notify-send -a System '{summary}' '{text}'")
        )
        if sound:
            asyncio.create_task(
                Utils.exec_sh_async(
                    "cvlc ~/.systemui/assets/sound/notification.mp3 --no-loop --no-repeat --play-and-exit"
                )
            )

    def low_battery_notify(self):
        if self.laptop_battery.charging:
            return

        if self.laptop_battery.percent <= self.battery_state["lower"]:
            self.notify(
                f"Battery is at {int(self.laptop_battery.percent)}%, charge now!"
            )
            return

        if (
            self.laptop_battery.percent <= self.battery_state["low"]
            and not self.notified["low bat"]
        ):
            self.notify(
                f"Battery is at {int(self.laptop_battery.percent)}%",
                sound=True,
            )
            self.notified["low bat"] = True

        if self.laptop_battery.percent > self.battery_state["low"]:
            self.notified["low bat"] = False

    def charging_notify(self):
        if self.laptop_battery.charging and not self.notified["charging"]:
            self.notify("Charging!")
            self.notified["charging"] = True
            return
        if not self.laptop_battery.charging:
            self.notified["charging"] = False

    def charged_notify(self):
        if (
            self.laptop_battery.percent >= self.battery_state["max"]
            and not self.notified["charged"]
            and self.laptop_battery.charging
        ):
            self.notify("Battery is fully charged!")
            self.notified["charged"] = True
            return

        if (
            self.laptop_battery.percent < self.battery_state["max"]
            and not self.laptop_battery.charging
        ):
            self.notified["charged"] = False
