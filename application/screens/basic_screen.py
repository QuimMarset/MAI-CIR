from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen


class BasicScreen(Screen):

    def __init__(self, screen_name, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_name = screen_name
        self.screen_manager = screen_manager
        self.__build_screen()


    def __build_screen(self):
        self.layout = AnchorLayout()
        self.add_widget(self.layout)


    def get_screen_name(self):
        return self.screen_name