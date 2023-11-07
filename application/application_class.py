from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from application.screens.screen_manager import CustomScreenManager
from application.widgets.action_bar import CustomActionBar
from constants import light_green_color, maroon_color


class ASLDetectorApp(App):


    def __init__(self, **kwargs):
        self.title = 'ASL Detector'
        super().__init__(**kwargs)


    def build(self):
        Window.clearcolor = light_green_color

        self.box_layout = BoxLayout(orientation='vertical') 

        self.action_bar = CustomActionBar()
        self.screen_manager = CustomScreenManager(self.action_bar)
        
        self.box_layout.add_widget(self.action_bar)
        self.box_layout.add_widget(self.screen_manager)
        
        return self.box_layout 