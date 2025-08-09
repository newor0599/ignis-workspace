from ignis.widgets import Widget


def tray_open_hitbox(self):
    Widget.Window(
        namespace="Tray Hitbox IGNIS",
        child=Widget.EventBox(
            css_classes=["tray-hitbox"],
            on_hover=lambda x: (setattr(self.visible["tray"], "value", True),),
        ),
        anchor=["top", "right"],
    )


def tray_close_hitbox(self):
    Widget.Window(
        namespace="Tray Close Hitbox IGNIS",
        child=Widget.EventBox(
            on_click=lambda x: (setattr(self.visible["tray"], "value", False),),
            css_classes=["tray-hitbox"],
        ),
        anchor=["top", "bottom", "left", "right"],
        visible=self.visible["tray"].bind("value", lambda x: x),
    )
