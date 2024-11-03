import sys
import os
from ignis.app import IgnisApp

style_path = os.path.expanduser("~/.config/ignis/main.scss")

IgnisApp.get_default().apply_css(style_path)

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(script_path)
from modules.bar import main 
from popups import backlight
from popups import volume
