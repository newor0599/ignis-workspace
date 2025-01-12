from collections.abc import Callable
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService


class Popup(Widget.Revealer):
    def __init__(
        self,
        value,
        icon,
        on_value_change: Callable,
        debug: bool = False,
        **kwargs,
    ):
        self.debug = debug
        self.callable_on_change = on_value_change
        self.timeout_popup = None
        scale = Widget.Scale(
            css_classes=["popup", "scale"],
            on_change=lambda x: self.callable_on_change(x.value),
            value=value,
            hexpand=True,
            **kwargs,
        )

        icon = Widget.Label(
            label=icon,
            css_classes=["popup", "icon"],
            valign="center",
            halign="center",
        )

        frame = Widget.Box(
            css_classes=["popup", "frame"],
            child=[
                icon,
                scale,
            ],
            # hexpand=True,
        )

        super().__init__(
            child=frame,
            transition_type="slide_up",
            transition_duration=200,
            css_classes=["popup", "revealer"],
        )

    def popup(self):
        if self.debug:
            return
        if self.timeout_popup is not None:
            self.timeout_popup.cancel()
        self.set_reveal_child(True)
        self.timeout_popup = Utils.Timeout(
            ms=1000, target=lambda: self.set_reveal_child(False)
        )


audio = AudioService.get_default()
speaker = audio.speaker
backlight = BacklightService.get_default()


def get_audio_icon(volume_level: int) -> str:
    if volume_level is None:
        return ""
    if volume_level <= 0:
        return " "
    if volume_level <= 50:
        return " "
    if volume_level <= 100:
        return " "
    if volume_level > 100:
        return "󱄡 "


def get_backlight_icon(backlight_level: int) -> str:
    if backlight_level <= 0:
        return "󰃞 "
    if backlight_level <= 50:
        return "󰃟 "
    if backlight_level <= 100:
        return "󰃠 "


def audio_popup() -> Popup:
    popup = Popup(
        value=speaker.bind("volume", lambda x: int(x) if x is not None else 0),
        icon=speaker.bind(
            "volume", lambda x: get_audio_icon(int(x) if x is not None else -1)
        ),
        on_value_change=speaker.set_volume,
    )
    speaker.connect("notify::volume", lambda x, y: popup.popup())
    popup.set_reveal_child(True)
    return popup


def backlight_popup() -> Popup:
    popup = Popup(
        value=backlight.bind("brightness", lambda x: int(x)),
        icon=backlight.bind(
            "brightness",
            lambda x: get_backlight_icon((100 / backlight.max_brightness) * int(x)),
        ),
        on_value_change=backlight.set_brightness,
        max=backlight.max_brightness,
    )
    backlight.connect("notify::brightness", lambda x, y: popup.popup())
    return popup
