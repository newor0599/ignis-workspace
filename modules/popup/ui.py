from ignis.variable import Variable
from . import logic
from ignis.widgets import Widget


class MAIN(logic.MAIN):
    def popup(self, state: dict[Variable]): ...
    def popup_bl(self) -> Widget.Revealer:
        icon = Widget.Label(
            label=self.bl_state["icon"].bind("value"),
            halign="center",
            css_classes=["label", "popup", "bl"],
        )
        scale = Widget.Scale(
            on_change=lambda x: setattr(
                self.backlight, "brightness", x.value * self.backlight.max_brightness
            ),
            min=0,
            max=1,
            step=0.05,
            css_classes=["scale", "popup", "bl"],
            value=self.bl_state["value"].bind("value"),
        )
        return Widget.Revealer(
            child=Widget.Box(
                child=[icon, scale],
                css_classes=["box", "popup", "bl"],
            ),
            transition_type="slide_up",
            reveal_child=self.bl_state["visible"].bind("value"),
        )

    """
    def popup_vol(self) -> Widget.Revealer:
        icon = Widget.Label(
            label=self.vol_icon.bind("value", lambda x: x),
            halign="center",
            css_classes=["label", "popup", "bl"],
        )
        scale = Widget.Scale(
            on_change=lambda x: self.bl_scale_change(x.value),
            min=0,
            max=1,
            step=0.05,
            css_classes=["scale", "popup", "bl"],
            value=self.backlight.bind(
                "brightness", lambda x: x / self.backlight.max_brightness
            ),
        )
        return Widget.Revealer(
            child=Widget.Box(
                child=[icon, scale],
                css_classes=["box", "popup", "bl"],
            ),
            transition_type="slide_up",
            reveal_child=self.bl_visible.bind("value", lambda x: x),
        )
    """

    def ui(self):
        bl_popup = self.popup_bl()

        Widget.Window(
            namespace="Popup IGNIS",
            child=Widget.Box(child=[bl_popup]),
            anchor=["bottom"],
        )


def main():
    popup = MAIN()
    popup.ui()
