from ignis.variable import Variable
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
from ignis.utils import Utils


class MAIN:
    def __init__(self):
        self.service_inits()

        # Backlight
        self.bl_state = {
            "name": "bl",
            "visible": Variable(value=False),
            "icon": Variable(value=""),
            "value": Variable(value=0.5),
            "change": lambda x: setattr(
                self.backlight,
                "brightness",
                x.value * self.backlight.max_brightness,
            ),
        }
        self.backlight.connect(
            "notify::brightness",
            lambda x, y: self.brightness_change(
                x.brightness / self.backlight.max_brightness
            ),
        )

        # Volume
        self.vol_state = {
            "name": "vol",
            "visible": Variable(value=False),
            "icon": Variable(value=""),
            "value": Variable(value=0.5),
            "change": lambda x: setattr(
                self.audio.speaker,
                "volume",
                x.value * 100,
            ),
        }
        self.audio.speaker.connect(
            "notify::volume",
            lambda x, u: self.volume_change(x.volume / 100, x.is_muted),
        )
        self.audio.speaker.connect(
            "notify::is-muted",
            lambda x, u: self.volume_change(x.volume / 100, x.is_muted),
        )

    def service_inits(self):
        self.audio = AudioService.get_default()
        self.backlight = BacklightService.get_default()

    def volume_change(self, volume, muted):
        icons = "󰖁 ", "󰕿 ", "󰖀 ", "󰕾 ", "󱄡 "
        volume *= 100
        if volume <= 0 or type(volume) is not float or muted:
            self.vol_state["icon"].value = icons[0]
        elif volume > 0 and volume <= 33:
            self.vol_state["icon"].value = icons[1]
        elif volume > 33 and volume <= 66:
            self.vol_state["icon"].value = icons[2]
        elif volume > 66 and volume <= 100:
            self.vol_state["icon"].value = icons[3]
        elif volume > 100:
            self.vol_state["icon"].value = icons[4]
        volume /= 100
        self.vol_state["visible"].value = True
        self.vol_state["value"].value = volume
        self.vol_popup_debounce()

    def brightness_change(self, brightness: int):
        icons = "󰃞 ", "󰃝 ", "󰃟 ", "󰃠 "
        self.bl_state["icon"].value = icons[int(brightness * 10 // 3)]
        self.bl_state["visible"].value = True
        self.bl_state["value"].value = brightness
        self.bl_popup_debounce()

    @Utils.debounce(1000)
    def bl_popup_debounce(self):
        self.bl_state["visible"].value = False

    @Utils.debounce(1000)
    def vol_popup_debounce(self):
        self.vol_state["visible"].value = False
