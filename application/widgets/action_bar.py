from os.path import join
from kivy.uix.actionbar import ActionBar, ActionPrevious
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty
from constants import icons_path, kv_files_path, maroon_color, medium_font_size, white_color


class CustomActionPrevious(ActionPrevious):
    previous_image = StringProperty(join(icons_path, 'previous.png'))


class CustomActionBar(ActionBar):

    background_color = ListProperty(maroon_color)
    title = StringProperty('')
    app_icon = StringProperty('')
    previous_icon = StringProperty(join(icons_path, 'previous.png'))
    main_icon = StringProperty(join(icons_path, 'main.png'))
    font_size = NumericProperty(medium_font_size)
    text_color = ListProperty(white_color)
    
    Builder.load_file(join(kv_files_path, 'action_bar.kv'))

    
    def set_screen_title(self, title):
        self.title = title