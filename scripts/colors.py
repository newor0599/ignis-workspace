from colorthief import ColorThief
from os import path, system
from subprocess import run


class ColorManager:
    def __init__(self):
        self.colors = []

    def update(self, wallpaper_path: str = None, theme: int = 0):
        rgb = sorted(ColorThief(wallpaper_path).get_palette(2, 60))
        if theme == 1:
            rgb[2], rgb[0] = rgb[0], rgb[2]
        hexa = [self.rgb2hex(i) for i in rgb.copy()]

        # Set ignis theme
        with open(path.expanduser("~/.config/ignis/colors.scss"), "w") as f:
            f.write(f"""$ui-aa:rgb{rgb[2]};
$ui-ab:rgb{rgb[1]};
$ui-con:rgb{rgb[0]};""")
        print("Ignis theme configured!")

        # Set mango theme
        with open(path.expanduser("~/.config/mango/colors.conf"), "w") as f:
            f.write(f"""focuscolor=0x{hexa[1]}ff
bordercolor=0x{hexa[2]}ff""")
        print("Mango theme configured!")

        # Set wofi theme
        with open(path.expanduser("~/.config/wofi/colors"), "w") as f:
            f.write(f"""#{hexa[2]}
#{hexa[1]}
#{hexa[0]}
#000000""")
        print("Wofi theme configured!")

        # Set kitty theme
        with open(path.expanduser("~/.config/kitty/colors.conf"), "w") as f:
            f.write(f"""background #{hexa[0]}
foreground #{hexa[2]}
cursor #{hexa[1]}
selection_background #{hexa[2]}
color0 #{hexa[0]}
color1 #ed8274
color2  #a6cc70
color3  #fad07b
color4  #6dcbfa
color5  #cfbafa
color6  #90e1c6
color7  #{hexa[1]}
color8 #686868
color9 #f28779
color10 #bae67e
color11 #ffd580
color12 #73d0ff
color13 #d4bfff
color14 #95e6cb
color15 #{hexa[2]}
selection_foreground #{hexa[0]}""")
        print("Kitty theme configured!")

        # Reload applications
        system("/bin/bash -c 'kill -SIGUSR1 \"$KITTY_PID\"'")
        system("mmsg -d reload_config")

    def rgb2hex(self, rgb: list[int]):
        r = max(0, min(255, rgb[0]))
        g = max(0, min(255, rgb[1]))
        b = max(0, min(255, rgb[2]))
        return "{:02x}{:02x}{:02x}".format(r, g, b)


if __name__ == "__main__":
    c = ColorManager()
    wp_path = (
        run(
            ["swww", "query"],
            text=True,
            capture_output=True,
        )
        .stdout.split(" ")[-1]
        .strip()
    )
    print(wp_path)
    ColorManager().update(wp_path, 0)
