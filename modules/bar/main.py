from ignis.widgets import Widget
from ignis.utils import Utils
from workspace import workspace_indicator
from ignis.services.hyprland import HyprlandService
import os
import datetime

hypr = HyprlandService()

file_dir,file_name = os.path.split(os.path.abspath(__file__))

one_minute = 1000*10*60
clock = Widget.Label(label="skibidi")
def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)
    
Utils.Poll(timeout=one_minute,callback=lambda x:update_clock())

dot = workspace_indicator(1)

bar = Widget.CenterBox(
        css_classes=['bar','main'],
        hexpand = True,
        start_widget = Widget.Box(
            css_classes = ['bar','left'],
            child = [clock],
            ),
        center_widget = Widget.EventBox(
            valign = 'end',
            css_classes = ['bar','center'],
            child = [workspace_indicator(i) for i in range(1,11)],
            )
        )

bar_main = Widget.EventBox(
            css_classes = ["bar","trigger"],
            on_hover = lambda x: x.child[0].set_reveal_child(True),
            on_hover_lost = lambda x: x.child[0].set_reveal_child(False),
            child = [Widget.Revealer(
                hexpand = True,
                child = bar,
                transition_type = "slide_up",
                transition_duration = 500,
                reveal_child = False,
                )]
            )



Widget.Window(
        namespace="Taskbar",
        layer = 'top',
        anchor = ['bottom','left','right'],
        css_classes = ["bar","window"],
        child = bar_main
        )

timeout_workspace = None
def show_workspace():
    global timeout_workspace
    bar_main.child[0].set_reveal_child(True)
    if timeout_workspace != None:
        timeout_workspace.cancel()
    timeout_workspace = Utils.Timeout(1000,lambda: bar_main.child[0].set_reveal_child(False))
hypr.connect("notify::active-workspace",lambda x,y: show_workspace())

