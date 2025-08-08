from ignis.services.notifications import NotificationService
from ignis.utils import Utils
from ignis.variable import Variable


class MAIN:
    def __init__(self):
        self.service_inits()
        self.notifs = Variable(value=[])

    def service_inits(self):
        self.notif = NotificationService.get_default()

    def close_notif(self, notif):
        notif.set_reveal_child(False)
        notifs = self.notifs.value
        notifs.remove(notif)
        Utils.Timeout(
            ms=notif.transition_duration + 1,
            target=lambda: (
                notif.unparent(),
                self.notifs.set_value(notifs),
            ),
        )

    def pprint_notif(self, notif):
        print("App:", notif.app_name)
        print("Title:", notif.summary)
        print("Body:", notif.body)
        print("Icon:", notif.icon)
