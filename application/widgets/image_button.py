import os
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from constants import kv_files_path, maroon_color, border_width, cream_color


class ImageButton(ButtonBehavior, AnchorLayout):        

    image_source = StringProperty('')
    border_color = ListProperty(maroon_color)
    border_width = NumericProperty(border_width)
    background_color = ListProperty(cream_color)

    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    background_disabled_normal = StringProperty('atlas://data/images/defaulttheme/button_disabled')
    background_disabled_down = StringProperty('atlas://data/images/defaulttheme/button_disabled_pressed')
    border = ListProperty([16, 16, 16, 16])
    
    Builder.load_file(os.path.join(kv_files_path, 'image_button.kv'))
