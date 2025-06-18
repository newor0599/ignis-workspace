from ignis.widgets import Widget
from os import system
from ignis.app import IgnisApp
from PIL import Image
from PIL import ImageFilter


# Configurable commands
class PowerMenu:
    def __init__(self):
        self.exit_gui_cmd = "riverctl exit"
        self.screen_get_cmd = "grim ss.png"
        self.app = IgnisApp.get_default()

        self.exit_gui_btn = Widget.EventBox(
            css_classes=["powermenu", "btn-rig"],
            vertical=True,
            child=[
                Widget.Label(
                    label=" ",
                    css_classes=["powermenu", "opt", "icon"],
                    valign="center",
                    vexpand=True,
                ),
                Widget.Label(
                    label="Shutdown",
                    css_classes=["powermenu", "opt", "desc"],
                    valign="end",
                ),
            ],
            on_click=lambda x: system(self.exit_gui_btn),
        )

        self.logout_btn = Widget.EventBox(
            css_classes=["powermenu", "btn-rig"],
            vertical=True,
            child=[
                Widget.Label(
                    label=" ",
                    css_classes=["powermenu", "opt", "icon"],
                    valign="center",
                    vexpand=True,
                ),
                Widget.Label(
                    label="Log Out",
                    css_classes=["powermenu", "opt", "desc"],
                    valign="end",
                ),
            ],
            on_click=lambda x: system(self.exit_gui_cmd + ";logout"),
        )

        self.pm_main = Widget.EventBox(
            css_classes=["powermenu", "window"],
            child=[
                self.exit_gui_btn,
                self.logout_btn,
            ],
            on_click=lambda x: self.pm_revealer.set_reveal_child(False),
        )

        self.pm_bg = Widget.Picture(
            image="ss.png",
            content_fit="cover",
        )

        self.pm_parent = Widget.Overlay(
            vexpand=True,
            hexpand=True,
            valign="center",
            halign="center",
            child=self.pm_bg,
            overlays=[
                self.pm_main,
            ],
        )

    def get_bg(self):
        print("Getting screenshot")
        system(self.screen_get_cmd)
        img = Image.open("ss.png")
        img = img.filter(ImageFilter.GaussianBlur(2))
        img.save("ss.png")

    def window(self):
        self.get_bg()
        return Widget.Window(
            anchor=["left", "top", "right", "bottom"],
            namespace="Powermenu IGNIS",
            visible=False,
            child=Widget.EventBox(
                child=[self.pm_parent],
                css_classes=["powermenu", "shadow"],
                on_click=lambda x: self.app.close_window("Powermenu IGNIS"),
            ),
            dynamic_input_region=False,
        )
