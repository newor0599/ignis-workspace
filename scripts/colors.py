from colorthief import ColorThief
from os import path, system


class ColorManager:
    def __init__(self):
        self.colors = []

    def update(self, wallpaper_path: str = None, theme: int = 0):
        colors = sorted(ColorThief(wallpaper_path).get_palette(2, 60))
        if theme == 1:
            colors[2], colors[0] = colors[0], colors[2]

        # Set ignis theme
        with open(path.expanduser("~/.config/ignis/colors.scss"), "w") as f:
            f.write(f"""$ui-aa:rgb{colors[2]};
$ui-ab:rgb{colors[1]};
$ui-con:rgb{colors[0]};""")

        # Set hyprlock theme
        with open(path.expanduser("~/.config/hypr/wallust.conf"), "w") as f:
            f.write(f"""$uia=rgb{colors[2]}
$uib=rgb{colors[1]}
$uic=rgb{colors[0]}
$wallpaper={wallpaper_path}""")

        # Set mango theme
        with open(path.expanduser("~/.config/mango/colors.conf"), "w") as f:
            f.write(f"""focuscolor=0x{self.rgb2hex(colors[1])[1:]}ff
bordercolor=0x{self.rgb2hex(colors[2])[1:]}ff""")
        system("mmsg -d reload_config")

        # Set wofi theme
        with open(path.expanduser("~/.config/wofi/colors"), "w") as f:
            f.write(f"""#{self.rgb2hex(colors[2])[1:]}
#{self.rgb2hex(colors[1])[1:]}
#{self.rgb2hex(colors[0])[1:]}
#000000""")

    def rgb2hex(self, rgb: list[int]):
        r = max(0, min(255, rgb[0]))
        g = max(0, min(255, rgb[1]))
        b = max(0, min(255, rgb[2]))
        return "${:02x}{:02x}{:02x}".format(r, g, b)


if __name__ == "__main__":
    bob = ColorManager()
    bob.update_color()
