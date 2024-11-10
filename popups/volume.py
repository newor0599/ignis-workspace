from ignis.services.audio import AudioService
from .popup import Popup
from ignis.widgets import Widget
audio = AudioService.get_default()
speaker = audio.speaker

audio_popup = Popup(
    "volume",
    "󰕾",
    speaker.bind("volume",lambda x: int(x) if x != None else 50),
    speaker.set_volume,
    transition_type="slide_left",
    step_ = 2,
    max_ = 200,
)

speaker.connect("notify::volume",lambda x,y: audio_popup.show_popup())
 
Widget.Window(
    namespace = "Volume Popup",
    anchor = ['right'],
    child = audio_popup.popup()
)
