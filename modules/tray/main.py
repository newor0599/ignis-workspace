from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.upower import UPowerService
from ignis.services.audio import AudioService
from ignis.services.hyprland import HyprlandService
from os import system as cmd

from .bluetooth_menu import BluetoothMenu
from .audio_menu import AudioMenu
import datetime

hypr = HyprlandService.get_default()
upw = UPowerService.get_default()
audio = AudioService.get_default()


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


class Tray(Widget.RevealerWindow):
    def __init__(self):
        ## Elements Variables
        self.notified_battery = False
        self.clock_update = 1000 * 60

        ## Element Services
        self.battery_device = upw.display_device

        ## Tray elements
        self.bluetooth_toggle = self.BluetoothMenuToggle()
        self.app_audio_mixer_toggle = self.AppAudioMixerToggle()
        self.bluetooth_menu = self.BluetoothRevealer()
        self.app_audio_mixer_menu = self.AppAudioMixerRevealer()
        self.menus = [self.bluetooth_menu, self.app_audio_mixer_menu]
        self.clock_chip = self.ClockChip()
        self.battery_chip = self.BatteryChip()
        self.main_menu = self.MainMenu()
        self.main_tray = self.MainTray()
        self.tray_revealer = self.TrayRevealer()

        ## Element Update Triggers
        audio.connect(
            "notify::apps",
            lambda x, y: self.app_audio_mixer_menu.child.update_menu(),
        )

        super().__init__(
            namespace="tasktray IGNIS",
            css_classes=["tray-window"],
            anchor=["top", "right", "bottom"],
            child=Widget.EventBox(
                child=[self.tray_revealer],
                on_hover=lambda x: self.tray_revealer.set_reveal_child(True),
                on_hover_lost=lambda x: self.tray_revealer.set_reveal_child(
                    self.main_menu.reveal_child
                ),
            ),
            revealer=self.tray_revealer,
        )

    def MainTray(self) -> Widget.Box:
        tray_main = Widget.Box(
            css_classes=["tray-main"],
            child=[
                self.main_menu,
                Widget.Box(
                    vertical=True,
                    child=[
                        self.clock_chip,
                        self.battery_chip,
                        self.app_audio_mixer_toggle,
                        self.bluetooth_toggle,
                    ],
                ),
            ],
        )
        return tray_main

    def TrayRevealer(self):
        return Widget.Revealer(
            child=self.main_tray,
            transition_type="slide_left",
            reveal_child=False,
            css_classes=["tray-revealer"],
        )

    def ClockChip(self):
        def get_time():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            return hour, minute

        time_poll = Utils.Poll(timeout=self.clock_update, callback=lambda x: get_time())
        clock_widget = chip_widget(
            value=time_poll.bind("output", lambda x: f"{x[0]}\n{x[1]}"),
        )
        return clock_widget

    def BatteryChip(self):
        battery_widget = chip_widget(
            value=self.battery_device.bind("percent", lambda value: f"{int(value)}"),
            icon=self.battery_device.bind(
                "charging", lambda value: "󰂄" if value else "󰁹"
            ),
        )
        self.battery_device.connect(
            "notify::percent", lambda x, y: low_batt_warning(x.percent)
        )
        return battery_widget

    def AppAudioMixerToggle(self):
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

        def toggle(active):
            self.app_audio_mixer_menu.set_reveal_child(active)
            self.app_audio_mixer_menu.child.update_menu()
            self.main_menu.reveal(active)

        audio_widget = Widget.ToggleButton(
            hexpand=False,
            halign="center",
            child=Widget.Label(label=" "),
            css_classes=["tray", "button"],
            on_toggled=lambda x, active: toggle(active),
        )
        return audio_widget

    def AppAudioMixerRevealer(self):
        return Widget.Revealer(
            child=AudioMenu(),
            css_classes=["aam", "menu", "revealer", "tray"],
        )

    def BluetoothMenuToggle(self):
        def toggle_menu(active):
            self.bluetooth_menu.set_reveal_child(active)
            self.main_menu.reveal(active)

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
            on_toggled=lambda x, active: toggle_menu(active),
        )
        return bluetooth_toggle

    def BluetoothRevealer(self):
        return Widget.Revealer(
            child=BluetoothMenu(),
            css_classes=["tray", "bt", "menu", "revealer"],
        )

    def MainMenu(self):
        main_menu = Widget.Revealer(
            transition_type="slide_left",
            css_classes=["tray", "main-menu"],
            child=Widget.Box(
                vertical=True,
                child=self.menus,
                css_classes=["tray", "menu-item"],
            ),
        )

        def reveal(value: bool):
            if value:
                main_menu.set_reveal_child(True)
                return
            for menu in self.menus:
                if menu.reveal_child:
                    return
            main_menu.set_reveal_child(False)

        main_menu.reveal = reveal

        return main_menu
