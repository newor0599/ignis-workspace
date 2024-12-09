from ignis.services.backlight import BacklightService
from .popup import Popup
from ignis.widgets import Widget

backlight = BacklightService.get_default()
backlight_popup = Popup(
        value = backlight.bind("brightness",lambda x: int(x)),
        icon = "",
        on_value_change = backlight.set_brightness,
        max = backlight.max_brightness,
        )
backlight_popup.transition_type = 'slide_right'

backlight.connect('notify::brightness',lambda x,y: backlight_popup.popup()) 
Widget.Window(
        namespace = "Backlight Popup IGNIS",
        anchor = ['left'],
        child = backlight_popup
        )
