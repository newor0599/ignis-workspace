from ignis.widgets import Widget
from ignis.utils import Utils
import os
import datetime

file_dir,file_name = os.path.split(os.path.abspath(__file__))

one_min = 1000*60

clock = Widget.Label(
        label="10:10",
        )

def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)


Utils.Poll(timeout=one_min,callback=lambda x:update_clock())
Widget.Window(
        namespace="Empty Workspace",
        exclusivity="normal",
        layer = 'background',
        child = Widget.EventBox(
            css_classes = ['empty','frame'],
            child = [
                clock
                ],
            on_hover = lambda x:x.add_css_class("hover"),
            on_hover_lost = lambda x:x.remove_css_class("hover"),
            )
        )
