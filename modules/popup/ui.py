from ignis.variable import Variable
from . import logic
from ignis.widgets import Widget


class MAIN(logic.MAIN):
    def popup(self, state: dict[Variable]):
        icon = Widget.Label(
            label=state["icon"].bind("value"),
            halign="center",
            css_classes=["label", "popup", state["name"]],
        )
        scale = Widget.Scale(
            on_change=lambda x: state["change"](x),
            min=0,
            max=1,
            step=0.05,
            css_classes=["scale", "popup", state["name"]],
            value=state["value"].bind("value"),
        )
        revealer = Widget.Revealer(
            child=Widget.Box(
                child=[icon, scale],
                css_classes=["box", "popup", state["name"]],
            ),
            transition_type="slide_up",
            reveal_child=state["visible"].bind("value"),
        )
        Widget.Window(
            namespace=f"Popup {state['name']} IGNIS",
            child=revealer,
            anchor=["bottom"],
        )

    def ui(self):
        bl_popup = self.popup(self.bl_state)
        vol_popup = self.popup(self.vol_state)


def main():
    popup = MAIN()
    popup.ui()
