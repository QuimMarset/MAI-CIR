from os.path import join
from application.screens.basic_screen import BasicScreen
from application.application_utils import create_grid_layout
from application.widgets.image_label_button import ImageLabelButton
from application.screens.games.games_sequence import GamesSequence
from application.screens.review.theory_screen import TheoryScreen
from application.screens.exams.exam import Exam
from application.screens.sign_detection.sign_detection_selector_screen import SignDetectionWithSelectorScreen
from application.screens.lessons.lesson_utils import *
from application.database.json_manager import JsonManager
from constants import icons_path




class LessonScreen(BasicScreen):

    def __init__(self, screen_name, screen_manager, lesson_name, sign_type, signs, **kwargs):
        super().__init__(screen_name, screen_manager, **kwargs)
        self.sign_type = sign_type
        self.lesson_name = lesson_name
        self.signs = signs
        self.__build_screen()
        self.disable_exam_button_if_completed()


    def __build_screen(self):
        self.grid_layout = create_grid_layout(cols=4, size_hint=(1, 0.5))
        
        self.button_theory = ImageLabelButton(image_source=join(icons_path, 'theory.png'), text='Theory', size_hint_x=0.25)
        self.button_games = ImageLabelButton(image_source=join(icons_path, 'games.png'), text='Games', size_hint_x=0.25)
        self.button_practise = ImageLabelButton(image_source=join(icons_path, 'practise.png'), text='Practise', size_hint_x=0.25)
        self.button_test = ImageLabelButton(image_source=join(icons_path, 'test.png'), text='Test', size_hint_x=0.25)

        self.button_theory.bind(on_release=self.theory_callback)
        self.button_games.bind(on_release=self.games_callback)
        self.button_practise.bind(on_release=self.practise_callback)
        self.button_test.bind(on_release=self.test_callback)

        self.grid_layout.add_widget(self.button_theory)                              
        self.grid_layout.add_widget(self.button_games)
        self.grid_layout.add_widget(self.button_practise)
        self.grid_layout.add_widget(self.button_test)
        self.layout.add_widget(self.grid_layout)


    def disable_exam_button_if_completed(self):
        json_manager = JsonManager()
        if json_manager.is_lesson_completed(self.lesson_name):
            self.button_test.disabled = True
    

    def theory_callback(self, *args):
        signs_video_paths_dict = create_signs_video_paths_dict(self.signs, self.sign_type)
        name = self.screen_name + ' - Theory'
        review_screen = TheoryScreen(name, self.screen_manager, self.lesson_name, signs_video_paths_dict)
        self.screen_manager.go_to_next_screen(review_screen)


    def games_callback(self, *args):
        signs_gif_paths_dict = create_signs_gif_paths_dict(self.signs, self.sign_type)
        name = self.screen_name + ' - Games'
        games = GamesSequence(name, self.screen_manager, self.lesson_name, signs_gif_paths_dict, self.sign_type)
        games.go_first_game()


    def practise_callback(self, *args):
        signs_gif_paths_dict = create_signs_gif_paths_dict(self.signs, self.sign_type)
        name = self.screen_name + ' - Practise Signs'
        sign_detection = SignDetectionWithSelectorScreen(name, self.screen_manager, 
            self.lesson_name, signs_gif_paths_dict, self.sign_type)
        self.screen_manager.go_to_next_screen(sign_detection)


    def test_callback(self, *args):
        signs_gif_paths_dict = create_signs_gif_paths_dict(self.signs, self.sign_type)
        name = self.screen_name + ' - Final Test'
        exam = Exam(name, self.screen_manager, self.lesson_name, signs_gif_paths_dict, self.sign_type)
        exam.go_first_question()
