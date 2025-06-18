import os
import sys

from ignis.app import IgnisApp
from ignis.widgets import Widget
from ignis.services.wallpaper import WallpaperService
from ignis.options import options

# Widgets
import modules.home_screen as home_screen_mod
import modules.popup as popup_mod
import modules.notification as notif_mod
import modules.tray.main as tray_mod
import modules.power_menu as power_menu

from colors import ColorManager
from modules import special_notif

file_dir, file_name = os.path.split(os.path.abspath(__file__))
special_notif.low_batt_warning()

# Theme configuration
theme = 0
color_shift = 7
selected_wallpaper = "red windows.jpg"

wallpaper_path = f"~/.systemui/assets/wallpapers/{selected_wallpaper}"
wallpaper_path = os.path.expanduser(wallpaper_path)
cm = ColorManager(wallpaper_path, color_id=color_shift)
cm.update_color(theme)
wallpaper = WallpaperService.get_default()
options.wallpaper.set_wallpaper_path(wallpaper_path)
style_path = os.path.expanduser("~/.config/ignis/main.scss")
IgnisApp.get_default().apply_css(style_path)
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts"))
sys.path.append(script_path)

notif_mod.desktop_notification()
home_screen_mod.home_screen(0)
tray = tray_mod.Tray()
pmmenu = power_menu.PowerMenu()
pmmenu.window()

audio = Widget.Window(
    namespace="Audio popups IGNIS",
    anchor=["bottom"],
    child=popup_mod.audio_popup(),
)
Widget.Window(
    namespace="Backlight popups IGNIS",
    anchor=["bottom"],
    child=popup_mod.backlight_popup(),
)

Widget.Window(
    namespace="TEST IGNIS",
    child=Widget.Box(css_classes=["test"]),
)
