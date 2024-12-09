import sys
import os
from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.services.notifications import notification

style_path = os.path.expanduser("~/.config/ignis/main.scss")

IgnisApp.get_default().apply_css(style_path)

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(script_path)
from modules.bar import main 
from modules.emptyworkspace import main
# from modules.popups import backlight
from modules.popups import volume
import modules.bar.main
# import modules.notification.notification
