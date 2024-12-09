from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.upower import UPowerService,UPowerDevice
from ignis.services.audio import AudioService
from workspace import workspace_indicator
from ignis.services.hyprland import HyprlandService
from .bluetooth_menu import BluetoothMenu
from .audio_menu import AudioMenu

import os
import datetime

hypr = HyprlandService()
upw = UPowerService.get_default()
audio = AudioService.get_default()

file_dir,file_name = os.path.split(os.path.abspath(__file__))

one_minute = 1000*60
clock = Widget.Label(label="Clock")
def get_time():
    hour = datetime.datetime.now().strftime("%H")
    minute = datetime.datetime.now().strftime("%M")
    return hour,minute

battery_device = upw.display_device

bt_menu = BluetoothMenu()
audios_menu = AudioMenu()

time_poll = Utils.Poll(timeout=one_minute,callback=lambda x:get_time())
class chip_widget(Widget.Box):
    def __init__(self,value,icon=""):
        value_label = Widget.Label(label = value,css_classes = ['bar-widget','value'])
        icon_label = Widget.Label(label = icon,css_classes = ['bar-widget','icon'])
        super().__init__(
                vertical = True,
                css_classes = ['bar-widget','frame'],
                valign='start',
                child = [
                    value_label,
                    icon_label if icon != "" else None
                    ]
                )

clock_widget = chip_widget(
        value = time_poll.bind('output',lambda x:f'{x[0]}\n{x[1]}')
        )

battery_widget = chip_widget(
        value = battery_device.bind('percent',lambda value: f'{int(value)}'),
        icon = battery_device.bind('charging',lambda value: "󰂄" if value else "󰁹")
        )

audio_widget = chip_widget(
        value = audio.speaker.bind('volume',lambda value:f'{int(value) if value != None else 50}'),
        icon = audio.speaker.bind('volume',lambda value: str((" " if value > 0 else " ") if value != None else "no speaker")),
        )

bar_main = Widget.Box(
        vertical = True,
        css_classes = ['bar-main'],
        child = [
            clock_widget,
            battery_widget,
            audio_widget,
            ]
        )

bar_revealer = Widget.Revealer(
        child = bar_main,
        transition_type = 'slide_left',
        reveal_child = False,
        )
Widget.RevealerWindow(
        namespace = "taskbar IGNIS",
        css_classes = ['bar-window'],
        anchor = ['top','right','bottom'],
        child = Widget.EventBox(
            child=[bar_revealer],
            style = 'padding: 10px;',
            on_hover = lambda x:bar_revealer.set_reveal_child(True),
            on_hover_lost = lambda x:bar_revealer.set_reveal_child(False)
            ),
        revealer = bar_revealer,
        )
bar_revealer.set_reveal_child(False)
