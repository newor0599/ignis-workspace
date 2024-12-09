import sys
import os
from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.services.notifications import notification
from ignis.widgets import Widget

style_path = os.path.expanduser("~/.config/ignis/main.scss")

IgnisApp.get_default().apply_css(style_path)

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(script_path)
from modules.bar import main 
from modules.emptyworkspace import main
# from modules.popups import backlight
from modules.popups import volume
import modules.bar.main
# import modules.notification.notification

reveal = Widget.Revealer(
        transition_type = 'slide_down',
        child = Widget.Box(
            style = 'background: #0da0ff;padding: 10px;margin: 10px;',
            vexpand = False,
            child = [
                Widget.Label(label = "You've found me"),
                Widget.Scale(
                    vertical = True,
                    inverted = True,
                    css_classes = ['popup','scale']
                    )
                ]
            )
        )
timeout = None
def timeout_reveal(_):
    global timeout, reveal
    if timeout != None:
        timeout.cancel()
    reveal.set_reveal_child(True)
    timeout = Utils.Timeout(ms=500,target = lambda: reveal.set_reveal_child(False))

Widget.Window(
        namespace = 'TEST IGNIS',
        anchor = ['top'],
        child = Widget.Box(
            vertical = True,
            child = [
                # Widget.Label(label = "Hello"),
                # Widget.Button(label = 'Find me',style = 'background:#ff99aa;padding: 10px;margin: 10px;',on_click = timeout_reveal),
                Widget.EventBox(
                    style = "padding: 10px; background: #03913a99;",
                    on_hover = lambda _:reveal.set_reveal_child(True),
                    on_hover_lost = lambda _:reveal.set_reveal_child(False),
                    ),
                reveal
                ]
            )
        )
