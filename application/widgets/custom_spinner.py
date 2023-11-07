from os.path import join
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.lang import Builder
from constants import *



class CustomSpinnerOption(SpinnerOption):

    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    background_color = ListProperty(cream_color)
    text_color = ListProperty(maroon_color)
    font_size = NumericProperty(small_font_size)

    Builder.load_file(join(kv_files_path, 'custom_spinner.kv'))



class CustomSpinner(Spinner):

    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    background_color = ListProperty(cream_color)
    label_text = StringProperty('Select a Sign')
    text_color = ListProperty(maroon_color)
    expand_arrow = StringProperty(join(icons_path, 'expand_arrow.png'))
    collapse_arrow = StringProperty(join(icons_path, 'collapse_arrow.png'))
    label_font_size = NumericProperty(small_font_size)

    Builder.load_file(join(kv_files_path, 'custom_spinner.kv'))