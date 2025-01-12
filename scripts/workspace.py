from ignis.widgets import Widget
from ignis.services.hyprland import HyprlandService

hypr = HyprlandService.get_default()


class workspace_indicator(Widget.EventBox):
    def __init__(self, id):
        self.id = id
        super().__init__(
            valign="center",
            css_classes=["workspace-indicator"],
            on_click=lambda x: self.workspace_clicked(),
        )
        hypr.connect("notify::active-workspace", lambda x, y: self.workspace_active())

    def workspace_clicked(self):
        self.add_css_class("active")
        hypr.switch_to_workspace(self.id)

    def workspace_active(self):
        if self.id == hypr.active_workspace["id"]:
            self.add_css_class("active")
        else:
            self.remove_css_class("active")
