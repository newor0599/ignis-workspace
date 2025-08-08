from modules.tray.ui import main as tray
from modules.popup.ui import main as popup
from modules.watermark.ui import main as watermark
from scripts import colors
from ignis.app import IgnisApp
from os import path

activation_watermark = False
tray()
popup()
if activation_watermark:
    watermark()
app = IgnisApp.get_default()
home_path = path.expanduser("~")
colors.ColorManager().update_color(0)
app.apply_css(f"{home_path}/.config/ignis/style.scss")
