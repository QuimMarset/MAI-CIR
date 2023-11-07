from os.path import join
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from constants import kv_files_path, maroon_color, cream_color, border_width, medium_font_size


class ImageLabelButton(ButtonBehavior, BoxLayout):        

    image_source = StringProperty('')
    text = StringProperty('')
    background_color = ListProperty(cream_color)
    text_color = ListProperty(maroon_color)
    border_color = ListProperty(maroon_color)
    border_width = NumericProperty(border_width)
    font_size = NumericProperty(medium_font_size)

    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    background_disabled_normal = StringProperty('atlas://data/images/defaulttheme/button_disabled')
    background_disabled_down = StringProperty('atlas://data/images/defaulttheme/button_disabled_pressed')
    border = ListProperty([16, 16, 16, 16])
    
    Builder.load_file(join(kv_files_path, 'image_label_button.kv'))
