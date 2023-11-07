from os.path import join
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, ListProperty, NumericProperty
from constants import kv_files_path, maroon_color, cream_color, border_width


class ImageToggleButton(ToggleButton):
    image_source = StringProperty('')
    border_color = ListProperty(maroon_color)
    border_width = NumericProperty(border_width)
    background_color = ListProperty(cream_color)

    Builder.load_file(join(kv_files_path, 'image_toggle_button.kv'))