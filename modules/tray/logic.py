from ignis.variable import Variable
from ignis.utils import Utils
from ignis.services.upower import UPowerService
import datetime


class BAR:
    def __init__(self):
        self.clock_refresh_rate = 1000 * 20
        self.service_inits()
        self.visible = Variable(value=False)
        self.time = Variable(value="00\n00")
        self.month = Variable(value="Sep")
        self.day = Variable(value="11")
        self.battery_icon = self.laptop_batt.bind_many(
            ["percent", "charging"],
            lambda x, y: self.get_batt_icon(),
        )
        Utils.Poll(
            self.clock_refresh_rate,
            lambda x: self.update_time(),
        )

    def service_inits(self):
        self.upower = UPowerService.get_default()
        self.laptop_batt = self.upower.display_device

    def get_batt_icon(self) -> str:
        percent = int(self.laptop_batt.percent // 10)
        charge_icons = "󰢟", "󰢜", "󰂆", "󰂇", "󰂈", "󰢝", "󰂉", "󰢞", "󰂊", "󰂋", "󰂅"
        if self.laptop_batt.charging:
            return charge_icons[percent] + "\U00002009"
        if percent == 10:
            return "󰁹"
        if percent == 0:
            return "󰂎"
        batt_level_code = 0x000F007A
        return chr(batt_level_code + percent - 1)

    def update_time(self):
        now = datetime.datetime.now()
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        month = now.strftime("%B")
        day = now.day
        self.time.value = f"{hour}\n{minute}"
        self.month.value = month[:3]
        self.day.value = str(day)
