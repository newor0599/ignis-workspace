from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.wallpaper import WallpaperService
import os
import datetime

file_dir,file_name = os.path.split(os.path.abspath(__file__))
wallpaper_path = "~/.config/ignis/wallpaper warning linux.png"
wallpaper_path = os.path.expanduser(wallpaper_path)

one_min = 1000*60

clock = Widget.Label(
        label="10:10",
        valign="center",
        halign="center",
        css_classes=["empty","clock"],
        )

wallpaper = WallpaperService.get_default()
wallpaper.set_wallpaper("/home/newor/.config/ignis/wallpaper warning linux.png")

def update_clock():
    time = datetime.datetime.now().strftime("%H:%M")
    clock.set_label(time)


Utils.Poll(timeout=one_min,callback=lambda x:update_clock())
Widget.Window(
        namespace="Empty Workspace",
        exclusivity="normal",
        layer = 'background',
        child = Widget.Box(
            child = [
                clock,
                ],
            )
        )
