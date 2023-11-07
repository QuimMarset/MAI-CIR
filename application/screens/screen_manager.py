from kivy.uix.screenmanager import ScreenManager
from application.screens.main_screen import MainScreen
from application.database.json_manager import JsonManager



class CustomScreenManager(ScreenManager):

    def __init__(self, action_bar, **kwargs):
        super().__init__(**kwargs)
        self.screen_stack = []
        self.action_bar = action_bar
        self.__bind_action_bar_buttons()
        self.__init_screen_stack()


    def __init_screen_stack(self):
        self.main_screen = MainScreen(self)
        self.screen_stack.append(self.main_screen)
        self.go_to_main_screen()


    def set_action_bar(self, action_bar):
        self.action_bar = action_bar


    def go_to_previous_screen(self, *args):
        if len(self.screen_stack) > 1:
            self.screen_stack.pop()
            screen = self.screen_stack[-1]
            self.switch_to(screen, direction='right')
            self.action_bar.set_screen_title(screen.get_screen_name())


    def get_current_screen_name(self):
        return self.screen_stack[-1].get_screen_name()


    def go_to_main_screen(self, *args):
        for _ in range(len(self.screen_stack) - 1):
            self.screen_stack.pop()
        self.switch_to(self.main_screen, direction='right')
        self.action_bar.set_screen_title(self.main_screen.get_screen_name())


    def go_to_next_screen(self, screen):
        self.screen_stack.append(screen)
        self.switch_to(screen, direction='left')
        self.action_bar.set_screen_title(screen.get_screen_name())


    def change_sub_screen(self, screen, save=False):
        if save:
            self.screen_stack.append(screen)
            self.action_bar.set_screen_title(screen.get_screen_name())
        self.switch_to(screen, direction='left')


    def __bind_action_bar_buttons(self):
        button_previous = self.action_bar.ids.previous
        button_main = self.action_bar.ids.main
        button_previous.bind(on_press=self.go_to_previous_screen)
        button_main.bind(on_press=self.go_to_main_screen)


    def go_to_lesson_from_exam(self, *args):
        self.go_to_previous_screen(*args)
        screen = self.screen_stack[-1]
        screen.disable_exam_button_if_completed()