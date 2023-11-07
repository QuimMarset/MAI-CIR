from os.path import join
from kivy.lang import Builder
from constants import kv_files_path
from kivy.clock import Clock
from application.screens.sign_detection.base_sign_detection_screen import BaseSignDetectorScreen
from application.widgets.yes_no_popup import YesNoPopup


class SignDetectionScreen(BaseSignDetectorScreen):

    Builder.load_file(join(kv_files_path, 'sign_detection_screen.kv'))


    def __init__(self, screen_name, screen_manager, sign_visual_dict, parent_function_omit, parent_function_continue, 
        rng, sign_type, **kwargs):
        
        self.rng = rng
        self.sign_visual_dict = sign_visual_dict
        self.__choose_sign()
        self.parent_function_omit = parent_function_omit
        self.parent_function_continue = parent_function_continue
        self.num_mistakes = 0
        super().__init__(screen_name, screen_manager, sign_type, **kwargs)


    def __choose_sign(self):
        signs = list(self.sign_visual_dict.keys())
        sign = self.rng.choice(signs)
        self.expected_sign = str(sign)


    def initialize_instructions(self):
        self.update_instructions('Press "Start Detection" to start, or "Continue" to omit this question')


    def create_yes_no_popup(self):
        YesNoPopup(self.finish_detection).open()


    def end_detection(self):
        Clock.unschedule(self.update_frame)
        self.parent_function_continue()


    def finish_detection(self):
        # Big number to ensure the question score in the exam will be 0
        self.num_mistakes = 999
        self.parent_function_omit()


    def get_num_mistakes(self):
        return self.num_mistakes


    def get_game_name(self):
        return 'SignDetection'