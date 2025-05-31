from ignis.widgets import Widget
from ignis.services.network import NetworkService
from ignis.utils import Utils


class NetworkMenu(Widget.Box):
    def __init__(self):
        self.network_service = NetworkService.get_default()
        self.options = Widget.Box(css_classes=["wifi", "options"])
        self.scroll = Widget.Scroll(css_classes=["wifi", "scroll"], child=self.options)
        super().__init__(
            vertical=True,
            css_classes=["wifi", "window"],
            child=[Widget.Label(label="Wi-Fi"), self.scroll],
        )

    @Utils.run_in_thread
    def wifi_option(self, wifi: NetworkService.wifi) -> Widget.EventBox:
        def click_event() -> None:
            pwd_rev.set_reveal_child(not pwd_rev.reveal_child)

        ssid = Widget.Label(label=wifi.ssid)
        status_icon = Widget.Label(
            label="  " if wifi.is_connected else "",
            halign="end",
        )
        texts = Widget.Box(child=[ssid, status_icon])
        password_input = Widget.Entry(
            placeholder="Enter Password (empty if open)",
            on_accept=lambda x: wifi.connect_to(x.text),
            visibility=False,
        )
        pwd_rev = Widget.Revealer(
            child=password_input,
            transition_type="slide_down",
        )
        main = Widget.EventBox(
            child=[texts, pwd_rev],
            on_click=lambda x: click_event(),
        )
        return main
