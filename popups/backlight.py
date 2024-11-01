from ignis.widgets import Widget
from ignis.services.backlight import BacklightService
from ignis.utils import Utils

class BacklightPopup(Widget.EventBox):
    def __init__(self):
        super().__init__(
                css_classes = ['popup','backlight'],
                )
        self.backlight = BacklightService.get_default()
        self.backlight.connect("notify::brightness", lambda x,y:self.timeout_popup())
        self.startup_locked = True
        self.popup_timeout = None
        self.reveal = Widget.Revealer(child = self.content(),css_classes = ['backlight','popup','reveal'],transition_type = 'slide_right',transition_duration = 300)
        print(self.backlight.max_brightness)

    def content(self) -> Widget.EventBox:
        icon = Widget.Label(label = "",css_classes = ['popup','backlight','icon'])
        bar = Widget.Scale(
                min = 0,
                max = self.backlight.max_brightness,
                step = 100,
                on_change = lambda x:self.backlight.set_brightness(bar.value),
                css_classes = ['popup','backlight','scale'],
                value = self.backlight.bind("brightness",lambda value: value),
                vertical = True
                )
        self.backlight.connect("notify::backlight", lambda x,y:print(x,y))
        return Widget.Box(
                    child = [bar,icon],
                    css_classes = ['backlight','popup','frame'],
                    vertical = True,
                )

    def timeout_popup(self):
        print(self.backlight.brightness)
        if self.popup_timeout != None:
            self.popup_timeout.cancel()
        self.reveal.set_reveal_child(True)
        self.popup_timeout = Utils.Timeout(800,lambda: self.reveal.set_reveal_child(False))

    def popup(self):
        return self.reveal
Widget.Window(
        namespace = "Backlight Popup",
        anchor = ['left'],
        child = BacklightPopup().popup()
        )
