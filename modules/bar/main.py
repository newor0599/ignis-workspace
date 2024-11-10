from ignis.widgets import Widget
from ignis.utils import Utils
from workspace import workspace_indicator
from ignis.services.hyprland import HyprlandService
from .bluetooth_menu import BluetoothMenu
from .audio_menu import AudioMenu
import os
import datetime

hypr = HyprlandService()

file_dir,file_name = os.path.split(os.path.abspath(__file__))

one_minute = 1000*10*60
clock = Widget.Label(label="Clock")
def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)
    
bt_menu = BluetoothMenu()
audios_menu = AudioMenu()

main_connection_menu = Widget.Box(
    halign = 'end',
    child = [
        Widget.Revealer(
            transition_type = 'slide_up'
        ),
    ]
)


def connection_menu_on(menu):
    if type(menu) == BluetoothMenu:
        menu._scan()
    if type(menu) == AudioMenu: #type: ignore
        menu.update_menu()

def toggle_connection_menu(menu):
    old_child = main_connection_menu.child[0].child
    main_connection_menu.child[0].set_child(menu)
    if old_child == menu:
        main_connection_menu.child[0].set_reveal_child(not main_connection_menu.child[0].reveal_child)
    if main_connection_menu.child[0].reveal_child:
        connection_menu_on(menu)

bar = Widget.CenterBox(
        css_classes=['bar','main'],
        hexpand = True,
        start_widget = Widget.Box(
            css_classes = ['bar','left'],
            child = [clock],
            ),
        center_widget = Widget.EventBox(
            valign = 'end',
            on_scroll_up = lambda x: hypr.switch_to_workspace(hypr.active_workspace['id']+1),
            on_scroll_down = lambda x: hypr.switch_to_workspace(hypr.active_workspace['id']-1),
            css_classes = ['bar','center'],
            child = [workspace_indicator(i) for i in range(1,11)],
            ),
        end_widget = Widget.Box(
            css_classes = ['bar','right'],
            valign = 'center',
            halign = 'center',
            child = [
                Widget.Button(
                    css_classes = ['bar','bt','trigger'],
                    child = Widget.Label(label = "󰂯"),
                    on_click = lambda x: toggle_connection_menu(bt_menu)
                    ),
                Widget.Button(
                    css_classes = ['bar','bt','trigger'],
                    child = Widget.Label(label = " "),
                    on_click = lambda x: toggle_connection_menu(audios_menu)
                    )
                ]
            )
        )

timeout_bar = None
def hide_bar(reveal):
    global timeout_bar
    if timeout_bar != None:
        timeout_bar.cancel()
    timeout_bar = Utils.Timeout(200,lambda: reveal(False))

def show_bar(reveal):
    global timeout_bar
    if timeout_bar != None:
        timeout_bar.cancel()
    reveal(True)

bar_main = Widget.EventBox(
        # on_click = lambda x: toggle_connection_menu(),
        vertical = True,
        vexpand = True,
        valign = 'end',
        child = [
            main_connection_menu,
            Widget.EventBox(
                vertical = True,
                css_classes = ["bar","trigger"],
                on_hover = lambda x: show_bar(x.child[0].set_reveal_child),
                on_hover_lost = lambda x: hide_bar(x.child[0].set_reveal_child),
                child = [
                        Widget.Revealer(
                            hexpand = True,
                            valign = 'end',
                            child = bar,
                            transition_type = "slide_up",
                            transition_duration = 300,
                            reveal_child = False,
                        ),
                    ]
            ),
            ]
        )

Widget.Window(
    namespace="Taskbar",
    monitor = 0,
    layer = 'top',
    anchor = ['bottom','left','right'],
    child = bar_main,
)

timeout_workspace = None
startup_locked = True
old_workspace = 0
def show_workspace():
    global timeout_workspace,old_workspace,startup_locked
    if startup_locked:
        startup_locked = False
        return
    if old_workspace == hypr.active_workspace['id']: #type: ignore
        return
    old_workspace = hypr.active_workspace['id'] #type: ignore
    update_clock()
    bar_main.child[1].child[0].set_reveal_child(True)
    if timeout_workspace != None:
        timeout_workspace.cancel()
    timeout_workspace = Utils.Timeout(1000,lambda:bar_main.child[1].child[0].set_reveal_child(False))

hypr.connect("notify::active-workspace",lambda x,y: show_workspace())
