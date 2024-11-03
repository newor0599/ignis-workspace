from collections.abc import Callable
from ignis.widgets import Widget
from ignis.utils import Utils

class Popup():
    def __init__(self,name:str,icon:str,value:int, on_change:Callable, min_:int=0, max_:int=100,step_:int=10,vertical:bool = True,transition_type = "slide_right"):
        self.startup_locked = -2
        self.popup_timeout = None
        self.value = value
        self.vertical = vertical
        self.callable = on_change
        self.icon = icon
        self.min = min_
        self.max = max_
        self.name = name
        self.transition_type = transition_type
        bar_width = 150
        bar_height = 10
        if self.vertical:
            bar_height,bar_width = bar_width,bar_height
        self.bar_style = f"min-width:{bar_width}px;min-height:{bar_height}px;"
        self.reveal = Widget.Revealer(child = self.content(),css_classes = [self.name,'popup','reveal'],transition_type = self.transition_type,transition_duration = 300)

    def content(self) -> Widget.EventBox:
        icon = Widget.Label(label = self.icon,css_classes = ['popup',self.name,'icon'])
        bar = Widget.Scale(
                min = self.min,
                max = self.max,
                step = 100,
                on_change = lambda x:self.callable(bar.value),
                css_classes = ['popup',self.name,'scale'],
                value = self.value,
                vertical = self.vertical,
                style = self.bar_style
                )
        return Widget.Box(
                    child = [bar,icon] if self.vertical else [icon,bar],
                    css_classes = [self.name,'popup','frame'],
                    vertical = self.vertical,
                )

    def show_popup(self):
        if self.startup_locked < 0:
            self.startup_locked += 1
            return
        if self.popup_timeout != None:
            self.popup_timeout.cancel()
        self.reveal.set_reveal_child(True)
        self.popup_timeout = Utils.Timeout(800,lambda: self.reveal.set_reveal_child(False))

    def popup(self):
        return self.reveal
