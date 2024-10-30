import sys
import os
from ignis.app import IgnisApp
from ignis.widgets import Widget

style_path = os.path.expanduser("~/.config/ignis/main.scss")

IgnisApp.get_default().apply_css(style_path)

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(script_path)
import modules.bar.main # Quickbar
import modules.emptyworkspace.main #Empty Workspace Widgets
# import modules.settings.main # Settings Window
