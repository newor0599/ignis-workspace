from ignis.utils import Utils
from . import logic
from ignis.widgets import Widget
from os.path import expanduser


def NOTIF_POPUP(notif):
    app_name = notif.app_name
    if notif.app_name == "System":
        icon_path = expanduser("~/.systemui/icons/system.png")
    else:
        icon_path = notif.icon
    if notif.app_name == "":
        app_name = notif.summary
    text = Widget.Box(
        vertical=True,
        child=[
            Widget.Label(
                label=app_name,
                halign="start",
                css_classes=["name"],
            ),
            Widget.Label(
                label=notif.body,
                halign="start",
                css_classes=["body"],
                ellipsize="end",
            ),
        ],
        css_classes=["title"],
    )
    icon = Widget.Icon(
        image=icon_path,
        pixel_size=50,
        valign="start",
        vexpand=True,
    )
    group = [
        Widget.Box(
            child=[icon, text],
        )
    ]
    preview_size = 6
    if notif.summary == "screenshot":
        ss_preview = Widget.Picture(
            image=notif.icon,
            width=16 * preview_size,
            height=9 * preview_size,
            content_fit="cover",
            halign="end",
        )
        group.append(ss_preview)

    group = Widget.EventBox(
        child=group,
        css_classes=["notif-box"],
        visible=True,
    )
    rev = Widget.Revealer(
        transition_type="slide_down",
        child=group,
        css_classes=["notif-rev"],
        transition_duration=350,
        halign="start",
    )
    return rev


class MAIN(logic.MAIN):
    def __init__(self):
        super().__init__()
        self.notif.connect(
            "new_popup",
            lambda x, y: self.update_notifications(y),
        )

    def update_notifications(self, notif):
        notif = NOTIF_POPUP(notif)
        notifs = self.notifs.value
        setattr(self.notifs, "value", notifs + [notif])
        notif.set_reveal_child(True)
        timeout = Utils.Timeout(ms=3000, target=lambda: self.close_notif(notif))
        setattr(
            notif.child,
            "on_click",
            lambda x: (
                timeout.cancel(),
                self.close_notif(notif),
            ),
        )

    def ui(self):
        self.box = Widget.Box(
            css_classes=["notif-main"],
            child=self.notifs.bind("value"),
            vertical=True,
        )
        Widget.Window(
            namespace="notification popup IGNIS",
            anchor=["top", "left"],
            child=self.box,
        )


def main():
    main = MAIN()
    main.ui()
