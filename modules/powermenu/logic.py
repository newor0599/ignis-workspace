from ignis.variable import Variable


class Main:
    def __init__(self):
        self.cmd = {
            "shutdown": "systemctl poweroff",
            "reboot": "systemctl reboot",
            "logout": "mmsg -q",
            "lock": "hyprlock",
            "sleep": "systemctl suspend",
        }
        self.show = Variable(value=False)
