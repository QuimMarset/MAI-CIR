from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from application.screens.basic_screen import BasicScreen
from application.views.recycle_view import CustomRecycleView
from constants import maroon_color, medium_font_size


class ReviewScreen(BasicScreen):

    def __init__(self, screen_name, screen_manager, sign_visual_dict, **kwargs):
        super().__init__(screen_name, screen_manager, **kwargs)
        self.__build_screen(sign_visual_dict)

    def __build_screen(self, sign_visual_dict):
        self.box_layout = BoxLayout(orientation='vertical')
        
        self.label = Label(bold=True, color=maroon_color, font_size=medium_font_size, 
            text='Click the desired button to learn how to perform a sign', size_hint_y=0.1)
        self.recycle_view = CustomRecycleView(sign_visual_dict, size_hint_y=0.9)
        
        self.box_layout.add_widget(self.label)
        self.box_layout.add_widget(self.recycle_view)
        self.add_widget(self.box_layout)
