from . import logic
from ignis.widgets import Widget
from ignis.variable import Variable


class POPUP(Widget.Revealer, logic.POPUP):
    def __init__(
        self, popup_name: str, popup_icon, popup_value: Variable, popup_on_change
    ):
        self.icon = Widget.Label(
            label=popup_icon,
            halign="center",
            css_classes=["label", "popup", popup_name],
        )
        self.scale = Widget.Scale(
            on_change=lambda x: popup_on_change(x.value),
            min=0,
            max=1,
            step=0.05,
            css_classes=["scale", "popup", popup_name],
            value=popup_value.value,
        )
        super().__init__(
            child=Widget.Box(
                child=[self.icon, self.scale],
                css_classes=["box", "popup", popup_name],
            ),
            transition_type="slide_up",
            # reveal_child=self.value.bind("value",lambda x:)
        )


class MAIN(logic.MAIN):
    def popup(self, name, icon, value, on_change) -> Widget.Revealer:
        icon = Widget.Label(
            label=icon,
            halign="center",
            css_classes=["label", "popup", name],
        )
        scale = Widget.Scale(
            on_change=lambda x: on_change(x.value),
            min=0,
            max=1,
            step=0.05,
            css_classes=["scale", "popup", name],
            value=value,
        )
        return Widget.Revealer(
            child=Widget.Box(
                child=[icon, scale],
                css_classes=["box", "popup", name],
            ),
            transition_type="slide_up",
            reveal_child=self.bl_visible.bind("value", lambda x: x),
        )

    def ui(self):
        bl_popup = self.popup(
            "bl",
            self.bl_icon,
            self.backlight.bind(
                "brightness",
                lambda x: x / self.backlight.max_brightness,
            ),
            self.bl_scale_change,
        )

        # vol_popup = self.popup(
        #     "vol",
        #     self.vol_icon,
        #     self.speaker_volume.value,
        #     self.bl_scale_change,
        # )

        Widget.Window(
            namespace="Popup IGNIS",
            child=Widget.Box(child=[bl_popup]),
            anchor=["bottom"],
        )


def main():
    popup = MAIN()
    popup.ui()
