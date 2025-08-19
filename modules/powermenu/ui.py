from ignis.variable import Variable
from ignis.widgets import Widget
from ignis.utils import Utils
from . import logic


class Main(logic.Main):
    def button(self, icon: str, label: str, action: str):
        main_icon = icon
        main_label = label.title()
        icon = Variable(value=main_icon)
        label = Variable(value=main_label)

        @Utils.debounce(2000)
        def debounce():
            icon.value = main_icon
            label.value = main_label

        main = Widget.EventBox(
            css_classes=["button"],
            child=[
                Widget.Label(
                    label=icon.bind("value", lambda x: x),
                    css_classes=["icon"],
                    halign="center",
                    valign="center",
                ),
                Widget.Label(
                    label=label.bind("value"),
                    halign="center",
                    valign="end",
                    css_classes=["label"],
                ),
            ],
            hexpand=False,
            vertical=True,
            on_click=lambda x: (
                setattr(icon, "value", ""),
                setattr(label, "value", f"Confirm {main_label.lower()}?"),
                debounce(),
            ),
            on_right_click=lambda x: (
                setattr(icon, "value", main_icon),
                setattr(label, "value", main_label),
            ),
            on_middle_click=lambda x: (
                Utils.exec_sh(action) if label.value.find("Confirm") >= 0 else None
            ),
        )
        return main

    def ui(self):
        Widget.Window(
            namespace="powermenu IGNIS",
            anchor=["top"],
            child=Widget.Revealer(
                child=Widget.Box(
                    child=[
                        self.button("  ", "shutdown", self.cmd["shutdown"]),
                        self.button("  ", "lock", self.cmd["lock"]),
                        self.button("  ", "reboot", self.cmd["reboot"]),
                        self.button("  ", "logout", self.cmd["logout"]),
                        self.button("󰤄 ", "sleep", self.cmd["sleep"]),
                    ],
                    spacing=20,
                    halign="center",
                    css_classes=["powermenu"],
                ),
                reveal_child=self.show.bind("value"),
            ),
            layer="overlay",
        )

    def hitbox(self):
        close = Widget.Window(
            namespace="powermenu hitbox IGNIS",
            anchor=["top", "left", "bottom", "right"],
            child=Widget.EventBox(
                on_click=lambda x: (
                    setattr(self.show, "value", False),
                    setattr(close, "visible", False),
                ),
                css_classes=["powermenu", "hitbox"],
            ),
            visible=False,
        )

        close.connect(
            "notify::visible",
            lambda x, y: setattr(self.show, "value", x.visible),
        )


def main():
    powermenu = Main()
    powermenu.hitbox()
    powermenu.ui()
