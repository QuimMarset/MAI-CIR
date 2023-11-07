import time
from functools import partial
from application.screens.review.review_screen import ReviewScreen
from application.database.json_manager import JsonManager



class TheoryScreen(ReviewScreen):

    def __init__(self, screen_name, screen_manager, lesson_name, sign_visual_dict, **kwargs):
        super().__init__(screen_name, screen_manager, sign_visual_dict, **kwargs)
        self.lesson_name = lesson_name
        self.start_screen_time = time.time()
        self.__bind_buttons_to_stop_timer()


    def __bind_buttons_to_stop_timer(self):
        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.bind(on_release=self.stop_time)
        button_main.bind(on_release=self.stop_time)


    def stop_time(self, *args):
        json_manager = JsonManager()
        practise_time = time.time() - self.start_screen_time
        json_manager.add_theory_time(self.lesson_name, practise_time)

        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.unbind(on_release=self.stop_time)
        button_main.unbind(on_release=self.stop_time)