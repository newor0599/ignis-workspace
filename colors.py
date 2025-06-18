from subprocess import run
from os.path import expanduser
import json
import colorsys


def clamp_color(hex_color: str, max_clamp_value: int = 1, min_clamp_value: int = 0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255

    h, l, s = colorsys.rgb_to_hls(r, g, b)  # noqa: E741
    l = max(min_clamp_value, min(max_clamp_value, l))  # noqa: E741
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{0:02x}{1:02x}{2:02x}".format(int(r * 255), int(g * 255), int(b * 255))


class ColorManager:
    def __init__(self, wallpaper_path: str, color_id=3):
        self.runable = True
        if wallpaper_path.split(".")[-1] not in ("jpg", "jpeg", "png"):
            self.runable = False
            return None
        dark_cmd = [
            "hellwal",
            "-i",
            wallpaper_path,
            "-j",
            "--skip-term-colors",
        ]
        dark_bg_cmd = [
            "hellwal",
            "-i",
            wallpaper_path,
            "-j",
            "-c",
            "-v",
            "--skip-term-colors",
        ]
        light_cmd = [
            "hellwal",
            "-i",
            wallpaper_path,
            "-l",
            "-j",
            "--skip-term-colors",
        ]

        dark_palette = run(
            dark_cmd,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dark_bg = run(
            dark_bg_cmd,
            capture_output=True,
            text=True,
        ).stdout.strip()
        light_palette = run(
            light_cmd,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if len(dark_palette) <= 0:
            print("Invalid Image")
            self.runable = False
            return

        # Json to Dict
        dark_palette = json.loads(dark_palette)
        dark_bg = json.loads(dark_bg)
        light_palette = json.loads(light_palette)

        # Contrast
        clamped_a = clamp_color(
            dark_palette["colors"][f"color{color_id}"],
            min_clamp_value=0.65,
        )
        clamped_b = clamp_color(
            dark_palette["colors"][f"color{color_id + 8}"],
            0.5,
        )

        # Base palette
        self.main_palette = {
            "a": clamped_a,
            "b": clamped_b,
            "contrast_dark": dark_palette["special"]["background"],
            "contrast_light": light_palette["special"]["background"],
        }

    def update_color(self, theme: int = 0):
        if not self.runable:
            print("Invalid Image")
            return
        with open(expanduser("~/.config/ignis/style/colors.scss"), "w") as f:
            generate = f"""
$ui-aa: {self.main_palette["a"]};
$ui-ab: {self.main_palette["b"]};
$ui-shadow: rgba($ui-ab,0.5);
"""
            if theme:
                generate += f"$ui-con: {self.main_palette['contrast_light']};"
            else:
                generate += f"$ui-con: {clamp_color(self.main_palette['a'], max_clamp_value=0.1)};"
            f.write(generate)
