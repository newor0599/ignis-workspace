from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.upower import UPowerService
from ignis.services.audio import AudioService
from ignis.services.hyprland import HyprlandService
from os import system as cmd

from .bluetooth_menu import BluetoothMenu
from .audio_menu import AudioMenu
import os
import datetime

hypr = HyprlandService.get_default()
upw = UPowerService.get_default()
audio = AudioService.get_default()

one_minute = 1000 * 60
clock = Widget.Label(label="Clock")


class Tray(Widget.Box):
    def __init__(self):
        pass


def get_time():
    hour = datetime.datetime.now().strftime("%H")
    minute = datetime.datetime.now().strftime("%M")
    return hour, minute


battery_device = upw.display_device


time_poll = Utils.Poll(timeout=one_minute, callback=lambda x: get_time())


class chip_widget(Widget.EventBox):
    def __init__(self, value, icon=""):
        value_label = Widget.Label(
            label=value,
            css_classes=["tray", "chip", "value"],
        )
        icon_label = Widget.Label(
            label=icon,
            css_classes=["tray", "chip", "icon"],
            halign="center",
            justify="fill",
        )
        super().__init__(
            vertical=True,
            css_classes=["tray", "chip", "frame"],
            valign="start",
            child=[value_label, icon_label if icon != "" else None],
        )


clock_widget = chip_widget(
    value=time_poll.bind("output", lambda x: f"{x[0]}\n{x[1]}"),
)


notified_battery = False


@Utils.run_in_thread
def low_batt_warning(value, warning_thres: int = 15, critical_thres: int = 5):
    global notified_battery
    if int(value) > warning_thres:
        notified_battery = False
        return
    if value <= critical_thres:
        cmd(
            f"notify-send System Battery\\ {int(value)}\\%\\ left\\.\\ Charge\\ now -i ~/.systemui/icons/system.png"
        )
        cmd("cvlc --play-and-exit ~/.config/ignis/sounds/notification.mp3")
    if notified_battery:
        return
    if value > critical_thres and value <= warning_thres:
        cmd(
            f"notify-send System Low\\ battery\\,\\ {int(value)}\\%\\ left -i ~/.systemui/icons/system.png"
        )
        cmd("cvlc --play-and-exit ~/.config/ignis/sounds/notification.mp3")
    notified_battery = True


battery_widget = chip_widget(
    value=battery_device.bind("percent", lambda value: f"{int(value)}"),
    icon=battery_device.bind("charging", lambda value: "󰂄" if value else "󰁹"),
)
battery_device.connect("notify::percent", lambda x, y: low_batt_warning(x.percent))


def get_audio_icon(volume_level: int) -> str:
    if volume_level is None:
        return ""
    if volume_level <= 0:
        return " "
    if volume_level <= 50:
        return " "
    if volume_level <= 100:
        return " "
    if volume_level > 100:
        return "󱄡 "


bt_menu = BluetoothMenu()
audios_menu = AudioMenu()
main_menu = Widget.Revealer(
    transition_type="slide_left",
    css_classes=["tray", "main-menu"],
    child=Widget.Box(
        vertical=True,
        css_classes=["tray", "menu-item"],
    ),
)


def toggle_menu(menu_name, set_child, show_child):
    global main_menu
    main_menu.child.set_child(
        [Widget.Label(label=menu_name, css_classes=["tray", "main-menu", "title"])]
    )
    main_menu.child.append(set_child)
    main_menu.set_reveal_child(show_child)


audio_widget = Widget.ToggleButton(
    hexpand=False,
    halign="center",
    child=Widget.Label(label=" "),
    css_classes=["tray", "button"],
    on_toggled=lambda x, active: toggle_menu("Apps Audio", audios_menu, active),
)

## BLUETOOTH ##
bluetooth_toggle = Widget.ToggleButton(
    hexpand=False,
    halign="center",
    child=Widget.Label(
        label="󰂯",
        hexpand=False,
        vexpand=False,
        halign="center",
        valign="center",
    ),
    css_classes=["tray", "button"],
    on_toggled=lambda x, active: toggle_menu("Bluetooth", bt_menu, active),
)

tray_main = Widget.Box(
    css_classes=["tray-main"],
    child=[
        main_menu,
        Widget.Box(
            vertical=True,
            child=[
                clock_widget,
                battery_widget,
                audio_widget,
                bluetooth_toggle,
            ],
        ),
    ],
)

tray_revealer = Widget.Revealer(
    child=tray_main,
    transition_type="slide_left",
    reveal_child=False,
    css_classes=["tray-revealer"],
)

audio.connect("notify::apps", lambda x, y: audios_menu.update_menu())


def tray():
    revealer = Widget.RevealerWindow(
        namespace="tasktray IGNIS",
        css_classes=["tray-window"],
        anchor=["top", "right", "bottom"],
        child=Widget.EventBox(
            child=[tray_revealer],
            on_hover=lambda x: tray_revealer.set_reveal_child(True),
            on_hover_lost=lambda x: tray_revealer.set_reveal_child(
                main_menu.reveal_child
            ),
        ),
        revealer=tray_revealer,
    )
    revealer.revealer.set_reveal_child(False)
    return revealer
