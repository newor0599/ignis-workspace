from ignis.variable import Variable
from ignis.utils import Utils
from ignis.services.upower import UPowerService
from ignis.services.audio import AudioService
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
            lambda x: self.update_time(),
        )

        # Audio
        self.speakers = {}
        self.mics = {}
        self.audio.connect("notify::speakers", lambda x, y: self.update_speakers())
        self.audio.connect("notify::microphones", lambda x, y: self.update_mics())
        self.speaker_list = Variable(value=[])
        self.mic_list = Variable(value=[])

    def calc_batt_life(self):
        life = self.laptop_batt.time_remaining / 60
        string = ""
        if life >= 60:
            string += f"{str(int(life // 60))} hour "
        if int(life % 60) > 0:
            string += f"{str(int(life % 60))} min "
        string += "left"
        self.battery_life.value = string

    def service_inits(self):
        self.upower = UPowerService.get_default()
        self.laptop_batt = self.upower.display_device
        self.audio = AudioService.get_default()

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

    def update_speakers(self):
        speakers = self.audio.speakers
        self.speaker_list.value = []
        speaker_list = []
        for i in speakers:
            self.speakers[i.description] = i
            speaker_list.append(i.description)
        self.speaker_list.value = speaker_list

    def update_mics(self):
        mics = self.audio.microphones
        self.mic_list.value = []
        mics_list = []
        for i in mics:
            self.mics[i.description] = i
            mics_list.append(i.description)
        self.mic_list.value = mics_list

    def change_speaker(self, speaker_description: str):
        self.audio.speaker = self.speakers[speaker_description]

    def change_mic(self, mic_description: str):
        self.audio.microphone = self.mics[mic_description]
