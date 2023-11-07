from os.path import join
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, StringProperty
from constants import kv_files_path, maroon_color, border_width, maroon_color_str, cream_color, medium_font_size


class CustomToggleButton(ToggleButton):
    
    border_color = ListProperty(maroon_color)
    border_width = NumericProperty(border_width)
    text_color = ListProperty(maroon_color)
    background_color = ListProperty(cream_color)
    text = StringProperty('')
    font_size = NumericProperty(medium_font_size)

    Builder.load_file(join(kv_files_path, 'custom_toggle_button.kv'))
