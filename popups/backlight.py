from ignis.services.backlight import BacklightService
from .popup import Popup
from ignis.widgets import Widget

backlight = BacklightService.get_default()
backlight_popup = Popup(
        "backlight",
        "",
        backlight.bind("brightness",lambda x: int(x)),
        backlight.set_brightness,
        max_ = backlight.max_brightness,
        step_ = 100
        )
backlight.connect('notify::brightness',lambda x,y: backlight_popup.show_popup()) 
Widget.Window(
        namespace = "Backlight Popup",
        anchor = ['left'],
        child = backlight_popup.popup()
        )
