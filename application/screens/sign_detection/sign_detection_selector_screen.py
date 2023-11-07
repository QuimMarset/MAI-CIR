from os.path import join
import time
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from application.screens.sign_detection.base_sign_detection_screen import BaseSignDetectorScreen
from application.database.json_manager import JsonManager
from constants import kv_files_path, light_green_color


class SignDetectionWithSelectorScreen(BaseSignDetectorScreen):

    spinner_values = ListProperty([])
    window_background = ListProperty(light_green_color)
    reference_image_source = StringProperty('')

    Builder.load_file(join(kv_files_path, 'sign_detection_selection_screen.kv'))


    def __init__(self, screen_name, screen_manager, lesson_name, sign_visual_dict, sign_type, **kwargs):
        super().__init__(screen_name, screen_manager, sign_type, **kwargs)
        self.sign_visual_dict = sign_visual_dict
        self.lesson_name = lesson_name
        self.spinner_values = list(self.sign_visual_dict.keys())
        self.num_errors = 0
        self.start_screen_time = time.time()
        self.__bind_buttons_to_stop_timer()
        self.__disable_start_button()


    def initialize_instructions(self):
        self.update_instructions('Select a sign to recognize and press "Start Detection"')
    

    def spinner_selection(self, selected_sign):
        self.ids.signs_spinner.label_text = selected_sign
        self.expected_sign = selected_sign
        self.reference_image_source = self.sign_visual_dict[selected_sign]
        self.__enable_start_button()


    def __bind_buttons_to_stop_timer(self):
        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.bind(on_release=self.stop_time)
        button_main.bind(on_release=self.stop_time)


    def stop_time(self, *args):
        json_manager = JsonManager()
        practise_time = time.time() - self.start_screen_time
        json_manager.add_practise_time(self.lesson_name, practise_time)

        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.unbind(on_release=self.stop_time)
        button_main.unbind(on_release=self.stop_time)


    def __disable_start_button(self):
        button = self.ids.start_detection_button
        button.disabled = True


    def __enable_start_button(self):
        button = self.ids.start_detection_button
        if button.disabled:
            button.disabled = False