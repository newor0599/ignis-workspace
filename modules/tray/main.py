from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.upower import UPowerService
from ignis.services.audio import AudioService
from ignis.services.hyprland import HyprlandService
from ignis.services.network import NetworkService

from .bluetooth_menu import BluetoothMenu
from .audio_menu import AudioMenu
from .network_menu import NetworkMenu
import datetime


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
            child=[value_label, icon_label if icon != "" else ""],
        )


class Tray(Widget.RevealerWindow):
    def __init__(self):
        ## Elements Variables
        self.notified_battery = False
        self.clock_rate = 1000 * 20

        ## Element Services
        self.hyprS = HyprlandService.get_default()
        self.upwS = UPowerService.get_default()
        self.audioS = AudioService.get_default()
        self.networkS = NetworkService.get_default()

        self.battery_device = self.upwS.display_device
        self.network_service = NetworkService.get_default()
        self.network_service.wifi.set_enabled(True)

        ## Tray elements
        self.bluetooth_menu = self.BluetoothRevealer()
        self.app_audio_mixer_menu = self.AppAudioMixerRevealer()
        self.network_menu = self.NetworkRevealer()

        self.bluetooth_toggle = self.BluetoothMenuToggle()
        self.app_audio_mixer_toggle = self.AppAudioMixerToggle()
        self.network_toggle = self.NetworkToggle()

        self.menus = [self.bluetooth_menu, self.app_audio_mixer_menu, self.network_menu]
        self.clock_chip = self.ClockChip()
        self.battery_chip = self.BatteryChip()
        self.main_menu = self.MainMenu()
        self.main_tray = self.MainTray()
        self.tray_revealer = self.TrayRevealer()

        ## Element Update Triggers
        self.audioS.connect(
            "notify::apps",
            lambda x, y: self.app_audio_mixer_menu.child.update_menu(),
        )

        super().__init__(
            namespace="tasktray IGNIS",
            css_classes=["tray-window"],
            anchor=["top", "right", "bottom"],
            dynamic_input_region=True,
            child=Widget.EventBox(
                child=[self.tray_revealer],
                on_hover=lambda x: self.tray_revealer.set_reveal_child(True),
                on_hover_lost=lambda x: self.tray_revealer.set_reveal_child(
                    self.main_menu.reveal_child
                ),
            ),
            revealer=self.tray_revealer,
        )
        Utils.Timeout(ms=1300, target=lambda: self.revealer.set_reveal_child(False))

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
                        self.network_toggle,
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

        time_poll = Utils.Poll(timeout=self.clock_rate, callback=lambda x: get_time())
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

    def NetworkToggle(self):
        def toggle_menu(active):
            self.network_menu.set_reveal_child(active)
            self.main_menu.reveal(active)

        def get_icon() -> str:
            if self.network_service.ethernet.is_connected:
                return "󰈀 "
            wifi_strenght = self.networkS.wifi.devices[0].ap.strength
            if wifi_strenght == 0:
                return "󰤭 "
            if wifi_strenght <= 25:
                return "󰤟 "
            if wifi_strenght <= 50:
                return "󰤢 "
            if wifi_strenght <= 75:
                return "󰤥 "
            if wifi_strenght <= 100:
                return "󰤨 "

        toggle = Widget.ToggleButton(
            hexpand=False,
            halign="center",
            child=Widget.Label(),
            css_classes=["tray", "button"],
            on_toggled=lambda x, active: toggle_menu(active),
        )
        self.networkS.wifi.devices[0].ap.connect(
            "notify::strength", lambda x, y: toggle.child.set_label(get_icon())
        )

        return toggle

    def NetworkRevealer(self) -> Widget.Revealer:
        return Widget.Revealer(child=NetworkMenu(), transition_type="slide_down")

    def MainMenu(self):
        main_menu = Widget.Revealer(
            transition_type="slide_left",
            css_classes=["tray", "main-menu"],
            child=Widget.Box(
                vertical=True,
                child=self.menus,
                css_classes=["tray", "menu-item"],
            ),
            reveal_child=False,
        )
        main_menu.set_reveal_child(False)

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
