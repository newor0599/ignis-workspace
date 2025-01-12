from ignis.widgets import Widget
from ignis.services.audio import AudioService
from ignis.services.audio import Stream
import re


class AudioMenu(Widget.Box):
    def __init__(self):
        self.audio = AudioService.get_default()
        self.apps_control = Widget.Box(
            hexpand=True,
            vexpand=True,
            vertical=True,
        )
        super().__init__(
            hexpand=True,
            vexpand=True,
            vertical=True,
            css_classes=["audio", "window"],
            child=[
                Widget.Scroll(
                    css_classes=["audio", "scroll"],
                    child=self.apps_control,
                    hexpand=True,
                    vexpand=True,
                )  # Scroll
            ],  # Child
        )  # Super

    def app_control(self, app: Stream) -> Widget.Box:
        app_desc = re.sub("^\\([0-9]+\\)", "", app.description)

        volume = Widget.Scale(
            css_classes=["audio", "control", "volume", "scale"],
            value=app.volume,
            # draw_value=True,
            # value_pos="right",
            on_change=lambda x: app.set_volume(int(x.value)),
            hexpand=True,
        )
        app_name = Widget.Label(
            label=f"{app.name}",
            css_classes=["audio", "control", "name"],
            halign="start",
        )
        app_desc = Widget.Label(
            label=app_desc,
            css_classes=["audio", "control", "desc"],
            halign="start",
            style="margin: 0 0 10px 10px; font-size: 17px;",
            ellipsize="middle",
        )
        main = Widget.Box(
            child=[app_name, app_desc, volume],
            css_classes=["audio", "control", "box"],
            vertical=True,
            hexpand=True,
        )
        return main

    def update_menu(self):
        self.apps = self.audio.apps
        apps_control = []
        for app in self.apps:  # type: ignore
            apps_control.append(self.app_control(app))
        self.apps_control.set_child(apps_control)
