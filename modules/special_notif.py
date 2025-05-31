from ignis.utils import Utils
from os import system as cmd
from ignis.services.upower import UPowerService


battery_cd = False


@Utils.run_in_thread
def low_batt_warning():
    print("Battery notif called")
    upwS = UPowerService.get_default()
    battery_device = upwS.display_device
    print(battery_device.percent)
    battery_device.connect("notify::percent", lambda x, y: run(x.percent))

    def run(value, warning_thres: int = 15, critical_thres: int = 5):
        global battery_cd
        print("Battery Special notification: ", value)
        if int(value) > warning_thres:
            battery_cd = False
            return
        if value <= critical_thres:
            cmd(
                f"notify-send System Battery\\ {int(value)}\\%\\ left\\.\\ Charge\\ now -i ~/.systemui/icons/system.png"
            )
            cmd(
                "cvlc --no-repeat --play-and-exit ~/.config/ignis/sounds/notification.mp3"
            )
        if battery_cd:
            return
        if value > critical_thres and value <= warning_thres:
            cmd(
                f"notify-send System Low\\ battery\\,\\ {int(value)}\\%\\ left -i ~/.systemui/icons/system.png"
            )
            cmd(
                "cvlc --no-repeat --play-and-exit ~/.config/ignis/sounds/notification.mp3"
            )
        battery_cd = True
