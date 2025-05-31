from ignis.widgets import Widget
from os import system

exit_gui_cmd = "riverctl exit"

exit_gui_btn = Widget.EventBox(
    css_classes=["powermenu", "btn-rig"],
    vertical=True,
    child=[
        Widget.Label(
            label="o",
            css_classes=["powermenu", "opt", "icon"],
            valign="center",
        ),
        Widget.Label(
            label="Shutdown",
            css_classes=["powermenu", "opt", "desc"],
            valign="end",
        ),
    ],
    on_click=lambda x: system(exit_gui_btn),
)

logout_btn = Widget.EventBox(
    css_classes=["powermenu", "btn-rig"],
    vertical=True,
    child=[
        Widget.Label(
            label=":)",
            css_classes=["powermenu", "opt", "icon"],
            valign="center",
        ),
        Widget.Label(
            label="Log Out",
            css_classes=["powermenu", "opt", "desc"],
            valign="end",
        ),
    ],
    on_click=lambda x: system(exit_gui_cmd + ";logout"),
)
pm_main = Widget.EventBox(
    css_classes=["powermenu", "window"],
    child=[
        exit_gui_btn,
        logout_btn,
    ],
    on_click=lambda x: pm_revealer.set_reveal_child(False),
)


pm_revealer = Widget.Revealer(
    transition_type="slide_down",
    child=pm_main,
    reveal_child=True,
    transition_duration=500,
    vexpand=True,
    hexpand=True,
    valign="start",
    halign="center",
)


def main():
    return Widget.Window(
        anchor=["left", "top", "right", "bottom"],
        namespace="Powermenu IGNIS",
        child=Widget.EventBox(
            child=[pm_revealer],
            css_classes=["powermenu", "shadow"],
            on_click=lambda x: pm_revealer.set_reveal_child(False),
        ),
        # dynamic_input_region=True,
    )
