from os.path import join
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.modalview import ModalView
from constants import maroon_color, light_green_color, cream_color, border_width, kv_files_path



class VideoPopup(ModalView):

    video_source = StringProperty('')
    background_color = ListProperty(light_green_color)
    button_color = ListProperty(cream_color)
    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    button_text = StringProperty('Close')

    Builder.load_file(join(kv_files_path, 'video_popup.kv'))


    def button_callback(self, *args):
        self.ids.player.state = 'stop'
        self.dismiss()
