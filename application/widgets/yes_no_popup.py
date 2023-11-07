from os.path import join
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from constants import (maroon_color, light_green_color, cream_color, 
    medium_font_size, border_width, kv_files_path)



class YesNoPopup(ModalView):

    background_color = ListProperty(light_green_color)
    button_color = ListProperty(cream_color)
    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    text_color = ListProperty(maroon_color)
    font_size = NumericProperty(medium_font_size)
    label_text = StringProperty('Are you sure you want to continue?')
    yes_button_text = StringProperty('Yes')
    no_button_text = StringProperty('No')

    Builder.load_file(join(kv_files_path, 'yes_no_popup.kv'))


    def __init__(self, parent_function, **kwargs):
        super().__init__(**kwargs)
        self.parent_function = parent_function


    def yes_button_callback(self, *args):
        self.parent_function(*args)
        self.dismiss()


    def no_button_callback(self, *args):
        self.dismiss()