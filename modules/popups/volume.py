from ignis.services.audio import AudioService
from ignis.utils import Utils
from .popup import Popup
from ignis.widgets import Widget
audio = AudioService.get_default()
speaker = audio.speaker

audio_popup = Popup(
        value = speaker.bind("volume"),
        icon = ' ',
        on_value_change=speaker.set_volume,
        halign = 'center'
        )
audio_popup.transition_type = 'slide_right'
 
window = Widget.Window(
    namespace = "Volume Popup IGNIS",
    anchor = ['left'],
    child = Widget.Box(
        child = [audio_popup]
        ),
)

speaker.connect("notify::volume",lambda x,y: audio_popup.popup())
