from ignis.variable import Variable
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
import asyncio
from ignis.utils import Utils


class POPUP:
    def __init__(self, service, signal_name: str):
        self.visible = Variable(value=False)
        self.visible_cooldown = None
        self.service = service
        self.signal_name = signal_name
        self.icon = Variable(value="")
        self.service.connect(
            f"notify::{self.signal_name}", lambda x, y: self.visible_true()
        )

    @Utils.debounce(1000)
    def visible_timeout(self):
        self.visible.value = False

    def visible_true(self):
        self.visible.value = True
        self.visible_timeout()


class MAIN:
    def __init__(self):
        self.service_inits()
        self.bl_visible_cd = None
        self.bl_visible = Variable(value=False)
        self.backlight.connect(
            "notify::brightness", lambda x, y: self.bl_visible_manager()
        )
        self.bl_icon = self.backlight.bind("brightness", lambda x: self.get_bl_icon())
        self.bl_popup = POPUP(self.backlight, "brightness")

    def service_inits(self):
        self.audio = AudioService.get_default()
        self.backlight = BacklightService.get_default()

    def get_vol_icon(self):
        icons = "󰖁 ", "󰕿 ", "󰖀 ", "󰕾 ", "󱄡 "
        vol = int(self.speaker.value.volume / 100 // 4)
        print(vol)

    def get_bl_icon(self):
        icons = "󰃞 ", "󰃝 ", "󰃟 ", "󰃠 "
        percent = int(
            self.backlight.brightness / self.backlight.max_brightness * 10 // 3
        )
        return icons[percent]

    def bl_scale_change(self, value: float):
        self.backlight.brightness = self.backlight.max_brightness * value

    def bl_visible_manager(self):
        if self.bl_visible_cd is not None:
            self.bl_visible_cd.cancel()
        self.bl_visible.value = True
        self.bl_visible_cd = Utils.Timeout(
            ms=1000,
            target=lambda: setattr(self.bl_visible, "value", False),
        )
