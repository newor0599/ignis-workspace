from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.notifications import NotificationService,Notification
notif = NotificationService.get_default()

"""
{'id': 27, 'app_name': 'notify-send', 'icon': '', 'summary': 'hello sup', 'body': '', 'actions': [], 'timeout': 5000, 'time': 1733449005.128117, 'urgency': 1}
"""

testNotif = Notification(id=1,app_name="System",icon="",summary='hewwo',body='',actions=[],timeout=5000,time=1733449005.128117,urgency=1,popup=[],dbus=None)

class NotificationBox(Widget.Box):
    def __init__(self,notif:Notification):
        dismiss_btn = Widget.Button(
                label = "Dismiss",
                on_click = self.destroy_box
                )
        super().__init__(
                css_classes = ['notif','main'],
                vertical = True,
                child = [
                    Widget.Label(label=notif.app_name.title()), #type: ignore
                    dismiss_btn
                    ]
                )
    def destroy_box(self,*args):
        print("Destroy box")
        self.destroy()


new_notif = NotificationBox(testNotif)
Widget.Window(
        namespace = "Notification IGNIS",
        child = Widget.Box(
            child = [
                new_notif
                ]
            )
        )
