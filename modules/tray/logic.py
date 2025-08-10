from ignis.variable import Variable
from ignis.utils import Utils
from ignis.services.upower import UPowerService
from ignis.services.audio import AudioService
from ignis.services.network import NetworkService
from ignis.services.applications import ApplicationsService
import datetime


class BAR:
    def __init__(self):
        self.service_inits()

        # Menu
        self.visible = {
            "tray": Variable(value=False),
            "menus": Variable(value=False),
            "date_menu": Variable(value=False),
            "batt_menu": Variable(value=False),
            "mixer_menu": Variable(value=False),
            "net_menu": Variable(value=False),
        }
        self.menus = [i for i in self.visible.keys() if "menu" in i[-4:]]

        # Time
        self.time = {
            "time": Variable(value="10\n10"),
            "month": Variable(value="Sep"),
            "day": Variable(value="11"),
            "clock_refresh_rate": 1000 * 20,
        }

        # Battery
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
            lambda x: self.get_time(),
        )

        # Audio
        self.sinks = {}
        self.sources = {}
        self.audio.connect("notify::speakers", lambda x, y: self.update_sinks())
        self.audio.connect("notify::microphones", lambda x, y: self.update_sources())
        self.sink_list = Variable(value=[])
        self.sink_icon = Variable(value="")
        self.source_list = Variable(value=[])
        self.source_icon = Variable(value="")
        self.sink = {
            "dropdown_list": Variable(value=[]),
            "icon": Variable(value=""),
            "reference": {},
        }
        self.audio.microphone.connect(
            "notify::is-muted", lambda x, y: self.get_source_icon()
        )
        self.audio.speaker.connect(
            "notify::is-muted", lambda x, y: self.get_sink_icon()
        )
        self.apps_mixer = []

        # WiFi
        self.wifi_strength = Variable(value=0)
        self.network_icon = Variable(value="")
        self.wifi_device.ap.connect(
            "notify::strength",
            lambda x, y: setattr(
                self.network_icon,
                "value",
                self.get_network_icon(x) if self.network.wifi.is_connected else "󰤮 ",
            ),
        )

    def calc_batt_life(self) -> str:
        life = self.laptop_batt.time_remaining / 60
        string = ""
        if life >= 60:
            string += f"{str(int(life // 60))} hour "
        if int(life % 60) > 0:
            string += f"{str(int(life % 60))} min "
        if string != "":
            string += "left"
        if string == "":
            string += "Unavailable"
        self.battery_life.value = string
        return string

    def service_inits(self):
        self.upower = UPowerService.get_default()
        self.laptop_batt = self.upower.display_device
        self.audio = AudioService.get_default()
        self.applications = ApplicationsService.get_default()
        self.network = NetworkService.get_default()
        self.wifi_device = self.network.wifi.devices[0]

    def get_app_icon(self, app_name: str):
        apps = self.applications.apps
        searched = self.applications.search(apps, app_name)
        if len(searched) <= 0:
            return "application-x-executable"
        return searched[0].icon

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

    def get_network_icon(self, ap) -> str:
        no_internet_icon = "󰤮"
        connected_icons = "󰤯", "󰤟", "󰤢", "󰤥", "󰤨"
        security_icons = "󰤬", "󰤡", "󰤤", "󰤧", "󰤪"
        warning_icons = "󰤫", "󰤠", "󰤣", "󰤦", "󰤩"
        return connected_icons[ap.strength // 21] + " "

    def get_time(self):
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

    def update_sinks(self):
        sinks = self.audio.speakers
        default = self.audio.speaker.description
        sink_list = []
        for i in sinks:
            self.sinks[i.description] = i
            sink_list.append(i.description)
        sink_list.remove(default)
        sink_list = [default] + sink_list
        self.sink_list.value = sink_list

    def update_sources(self):
        sources = self.audio.microphones
        sources_list = []
        default = self.audio.microphone.description
        for i in sources:
            self.sources[i.description] = i
            sources_list.append(i.description)
        sources_list.remove(default)
        sources_list = [default] + sources_list
        self.source_list.value = sources_list

    def get_source_icon(self):
        if self.audio.microphone.is_muted:
            self.source_icon.value = "󰍭"
        else:
            self.source_icon.value = ""

    def get_sink_icon(self):
        if self.audio.speaker.is_muted:
            self.sink_icon.value = "󰓄"
        else:
            self.sink_icon.value = "󰓃"
