from ignis.variable import Variable
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
import asyncio
from ignis.utils import Utils


class MAIN:
    def __init__(self):
        self.service_inits()

        # Backlight
        self.bl_state = {
            "visible": Variable(value=False),
            "icon": Variable(value=""),
            "value": Variable(value=0.5),
        }
        self.backlight.connect(
            "notify::brightness",
            lambda x, y: self.brightness_change(
                x.brightness / self.backlight.max_brightness
            ),
        )

    @Utils.debounce(1000)
    def bl_timeout(self):
        self.bl_state["visible"].value = False

    def service_inits(self):
        self.audio = AudioService.get_default()
        self.backlight = BacklightService.get_default()
        # self.audio.speaker.connect(
        #     "notify::description", lambda x, y: print(x.description)
        # )
        # self.audio.speaker.connect("notify::volume", lambda x, y: print(x.volume))

    def get_vol_icon(self, volume):
        icons = "󰖁 ", "󰕿 ", "󰖀 ", "󰕾 ", "󱄡 "
        if volume == 0 or type(volume) is not int:
            return icons[0]
        if volume > 0 and volume <= 33:
            return icons[1]
        if volume > 33 and volume <= 66:
            return icons[2]
        if volume > 66 and volume <= 100:
            return icons[3]
        return icons[-1]

    def brightness_change(self, brightness: int):
        icons = "󰃞 ", "󰃝 ", "󰃟 ", "󰃠 "
        self.bl_state["icon"].value = icons[int(brightness * 10 // 3)]
        self.bl_state["visible"].value = True
        self.bl_state["value"].value = brightness
        self.bl_popup_debounce()

    def bl_scale_change(self, value: float):
        self.backlight.brightness = self.backlight.max_brightness * value

    @Utils.debounce(1000)
    def bl_popup_debounce(self):
        self.bl_state["visible"].value = False
