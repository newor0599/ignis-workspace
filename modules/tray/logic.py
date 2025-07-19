from ignis.variable import Variable
from ignis.utils import Utils
from ignis.services.upower import UPowerService
import datetime


class BAR:
    def __init__(self):
        self.service_inits()
        self.visible = {
            "tray": Variable(value=False),
            "menus": Variable(value=False),
            "date_menu": Variable(value=False),
            "batt_menu": Variable(value=False),
        }
        self.menus = [i for i in self.visible.keys() if "menu" in i[-4:]]
        self.time = {
            "time": Variable(value="10\n10"),
            "month": Variable(value="Sep"),
            "day": Variable(value="11"),
            "clock_refresh_rate": 1000 * 20,
        }
        self.battery_life = Variable(value="0 min")
        self.calc_batt_life()
        self.battery_icon = self.laptop_batt.bind_many(
            ["percent", "charging"],
            lambda x, y: self.get_batt_icon(),
        )
        self.laptop_batt.connect(
            "notify::time-remaining", lambda x, y: self.calc_batt_life()
        )
        Utils.Poll(
            self.time["clock_refresh_rate"],
            lambda x: self.update_time(),
        )

    def calc_batt_life(self):
        life = self.laptop_batt.time_remaining / 60
        string = ""
        if life >= 60:
            string += f"{str(int(life // 60))} hour "
        string += f"{str(int(life % 60))} min left"
        self.battery_life.value = string

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
        self.time["time"].value = f"{hour}\n{minute}"
        self.time["month"].value = month[:3]
        self.time["day"].value = str(day)

    def menu_visibility(self):
        visible = False
        for i in self.menus:
            if self.visible[i].value:
                visible = True
        self.visible["menus"].value = visible
