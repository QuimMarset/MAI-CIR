from os.path import join
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from constants import (maroon_color, light_green_color, cream_color, 
    medium_font_size, border_width, kv_files_path)



class ContinuePopup(ModalView):

    background_color = ListProperty(light_green_color)
    button_color = ListProperty(cream_color)
    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    text_color = ListProperty(maroon_color)
    font_size = NumericProperty(medium_font_size)
    label_text = StringProperty('Good job!')
    button_text = StringProperty('Continue')

    Builder.load_file(join(kv_files_path, 'continue_popup.kv'))


    def __init__(self, parent_function, **kwargs):
        super().__init__(**kwargs)
        self.parent_function = parent_function


    def button_callback(self, *args):
        self.parent_function(*args)
        self.dismiss()
