from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.notifications import NotificationService, Notification
from ignis.options import options
import os

notif = NotificationService.get_default()

"""
{'id': 27, 'app_name': 'notify-send', 'icon': '', 'summary': 'hello sup', 'body': '', 'actions': [], 'timeout': 5000, 'time': 1733449005.128117, 'urgency': 1}
"""


class NotificationBox(Widget.EventBox):
    def __init__(self, notif: Notification):
        self.notif = notif
        pp_notif(notif)
        body = Widget.Box(
            css_classes=["notif", "top-right"],
            vertical=True,
            child=[
                Widget.Label(
                    label=f"{notif.summary}",
                    css_classes=["notif", "app-name"],
                    hexpand=True,
                    halign="start",
                    ellipsize="end",
                ),
                Widget.Label(
                    label=notif.body,
                    css_classes=["notif", "body"],
                    vexpand=True,
                    valign="start",
                    halign="start",
                    wrap=True,
                    wrap_mode="word_char",
                ),
            ],
        )
        icon = Widget.Picture(
            image=notif.icon,
            css_classes=["notif", "icon"],
            valign="start",
            width=32,
            height=32,
            content_fit="cover",
        )

        top_frame = Widget.Box(
            child=[
                icon,
                body,
            ]
        )

        actions = None
        # Screenshot Layout
        if notif.app_name == "grimblast":
            icon.set_image(os.path.expanduser("~/.systemui/icons/system.png"))
            body.child[0].set_label("System")
            body.child[1].set_label(notif.summary)
            actions = Widget.Picture(
                image=notif.icon,
                width=1920 // 7,
                height=1080 // 7,
                content_fit="cover",
                css_classes=["notif", "image"],
            )

        if len(notif.actions) > 0:
            actions = self.create_actions(notif)
        super().__init__(
            vertical=True,
            css_classes=["notif", "main"],
            child=[top_frame],
            halign="end",
        )
        if actions is not None:
            super().append(actions)

    def destroy_box(self, *args):
        self.child[0].unparent()

    def create_actions(self, notif: Notification) -> Widget.Box:
        actions = Widget.Box(
            hexpand=True,
            halign="end",
            vexpand=True,
            valign="end",
        )
        for i in range(3):
            if i < len(notif.actions):
                button = Widget.Button(
                    child=Widget.Label(label=notif.actions[i].label, ellipsize="end"),
                    on_click=lambda x: notif.actions[i].invoke(),
                    css_classes=["notif", "action"],
                )
                actions.append(button)
        return actions


notifications_list = []


class Popup_notif(Widget.Revealer):
    def __init__(self, notif_box: NotificationBox):
        super().__init__(
            child=notif_box,
            reveal_child=False,
            transition_type="slide_down",
            transition_duration=400,
        )
        Utils.Timeout(ms=10, target=lambda: self.set_reveal_child(True))
        Utils.Timeout(
            ms=notif_box.notif.timeout,
            target=self.hide_notif,
        )

    def hide_notif(self):
        self.set_transition_type("slide_up")
        self.set_reveal_child(False)
        Utils.Timeout(ms=self.transition_duration, target=self.unparent)


notif.connect(
    "notified",
    lambda x, y: notif_master.prepend(Popup_notif(NotificationBox(y))),
)

notif_master = Widget.Box(vertical=True, style="background: #00000001;")


def desktop_notification():
    return Widget.Window(
        namespace="Notification IGNIS",
        layer="top",
        child=notif_master,
        anchor=["top", "left"],
    )


def pp_notif(notif: Notification):
    print("App name:", notif.app_name)
    print("Title:", notif.summary)
    print("Message:", notif.body)
    print("Actions:", [i.label for i in notif.actions])
    print("Icon:", notif.icon)
