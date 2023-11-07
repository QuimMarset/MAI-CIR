from os.path import join
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, StringProperty
from constants import kv_files_path, cream_color, maroon_color, border_width, medium_font_size


class CustomButton(Button):
    
    border_color = ListProperty(maroon_color)
    border_width = NumericProperty(border_width)
    background_color = ListProperty(cream_color)
    text = StringProperty('')
    text_color = ListProperty(maroon_color)
    font_size = NumericProperty(medium_font_size)

    Builder.load_file(join(kv_files_path, 'custom_button.kv'))