from ignis.utils import Utils
from modules.tray.ui import main as tray
from modules.popup.ui import main as popup
from modules.watermark.ui import main as watermark
from modules.notif.ui import main as notif
from modules.powermenu.ui import main as powermenu
from modules.homescreen.ui import main as homescreen
from scripts import colors
from scripts import system_notifications
from ignis.app import IgnisApp
from os import path

activation_watermark = 0
themer = 1
tray()
popup()
notif()
powermenu()
homescreen()

if activation_watermark:
    watermark()
app = IgnisApp.get_default()
home_path = path.expanduser("~")
if themer:
    wp_path = " ".join(Utils.exec_sh("swww query").stdout.split(" ")[7:]).strip()
    colors.ColorManager().update(wp_path, 0)
app.apply_css(f"{home_path}/.config/ignis/style.scss")
system_notifications.SYSTEM_NOTIF()
