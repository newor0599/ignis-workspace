from modules.tray.ui import main as tray
from modules.popup.ui import main as popup
from modules.watermark.ui import main as watermark
from ignis.app import IgnisApp
from os import path
from ignis.widgets import Widget

activation_watermark = False
tray()
popup()
if activation_watermark:
    watermark()
app = IgnisApp.get_default()
home_path = path.expanduser("~")
app.apply_css(f"{home_path}/.config/ignis/style.scss")
