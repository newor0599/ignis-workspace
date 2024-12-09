from collections.abc import Callable
from ignis.widgets import Widget
from ignis.utils import Utils

class Popup(Widget.Revealer):
    def __init__(self,value,icon:str,on_value_change:Callable,**kwargs):
        self.callable_on_change = on_value_change
        self.timeout_popup = None
        scale = Widget.Scale(
                vertical = True,
                css_classes = ['popup','scale'],
                inverted = True,
                on_change = lambda x: self.value_change(x),
                value = value,
                **kwargs
                )

        icon = Widget.Label(
                label = icon,
                css_classes = ['popup','icon'],
                )

        frame = Widget.Box(
                vertical = True,
                css_classes = ['popup','frame'],
                child = [scale,icon,],
                hexpand = True,
                style = 'margin: 0px 10px;'
                )
        super().__init__(
                child = frame,
                transition_type = "slide_left",
                transition_duration = 200
                )

    def popup(self):
        if self.timeout_popup != None:
            self.timeout_popup.cancel()
        self.show_popup()
        self.timeout_popup = Utils.Timeout(500,lambda: self.hide_popup())

    def show_popup(self):
        self.set_reveal_child(True)

    def hide_popup(self):
        self.set_reveal_child(False)

    def value_change(self,value):
        self.popup()
        self.callable_on_change(value.value)
