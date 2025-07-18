from modules.tray.ui import main as tray
from modules.popup.ui import main as popup
from ignis.app import IgnisApp
from os import path

tray()
popup()
app = IgnisApp.get_default()
home_path = path.expanduser("~")
app.apply_css(f"{home_path}/.config/ignis/style.scss")
