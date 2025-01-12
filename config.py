import os
import sys
from ignis.app import IgnisApp
from ignis.widgets import Widget
from ignis.services.wallpaper import WallpaperService
from ignis.options import options

# Widgets
from modules.home_screen import home_screen
from modules.popup import audio_popup
from modules.popup import backlight_popup
from modules.notification import desktop_notification
from modules.tray.main import tray

style_path = os.path.expanduser("~/.config/ignis/main.scss")
IgnisApp.get_default().apply_css(style_path)
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts"))
sys.path.append(script_path)

# Wallpaper
selected_wallpaper = "wallpaper.jpg"
file_dir, file_name = os.path.split(os.path.abspath(__file__))
wallpaper_path = f"~/.systemui/wallpapers/{selected_wallpaper}"
wallpaper_path = os.path.expanduser(wallpaper_path)
wallpaper = WallpaperService.get_default()
options.wallpaper.set_wallpaper_path(wallpaper_path)

desktop_notification()
home_screen(0)
tray()

Widget.Window(
    namespace="Audio popups IGNIS",
    anchor=["bottom"],
    child=audio_popup(),
)
Widget.Window(
    namespace="Backlight popups IGNIS",
    anchor=["bottom"],
    child=backlight_popup(),
)
