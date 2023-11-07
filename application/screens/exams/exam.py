import numpy as np
import time
from application.widgets.continue_popup import ContinuePopup
from application.screens.results.results_exam_screen import ResultsExamScreen
from application.screens.games.games_utils import *
from application.screens.sign_detection.sign_detection_screen import SignDetectionScreen
from application.database.json_manager import JsonManager
from constants import num_exam_questions, seed, penalization_sign, penalization_game, num_max_questions_detection


class Exam:

    def __init__(self, screen_name, screen_manager, lesson_name, sign_visual_dict, sign_type, **kwargs):
        self.screen_manager = screen_manager
        self.screen_name = screen_name
        self.lesson_name = lesson_name
        self.sign_visual_dict = sign_visual_dict
        self.sign_type = sign_type
        self.current_question = 0
        self.rng = np.random.default_rng(seed)
        self.__create_exam()

    
    def __create_sign_detection_questions(self):
        num_questions_detection = self.rng.integers(1, num_max_questions_detection+1)
        for _ in range(num_questions_detection):
            question = SignDetectionScreen(self.screen_name, self.screen_manager, 
                self.sign_visual_dict, self.advance_sequence, self.create_popup, 
                self.rng, self.sign_type)
            self.questions.append(question)


    def __create_non_sign_detection_questions(self):
        available_questions = get_available_games(self.sign_type)
        num_questions_non_sign = num_exam_questions - len(self.questions)
        non_sign_questions = self.__select_questions_randomly(num_questions_non_sign, available_questions)
        
        for question_class in non_sign_questions:
            question = question_class(self.screen_name, self.sign_visual_dict, self.create_popup, self.rng)
            self.questions.append(question)


    def __create_exam(self):
        self.questions = []
        self.__create_sign_detection_questions()
        self.__create_non_sign_detection_questions()
        self.rng.shuffle(self.questions)


    def create_popup(self):
        ContinuePopup(self.advance_sequence).open()


    def go_first_question(self):
        self.start_time = time.time()
        self.screen_manager.change_sub_screen(self.questions[self.current_question], save=True)


    def advance_sequence(self):
        self.current_question += 1

        if self.current_question < num_exam_questions:
            self.__go_next_question()
        else:
            self.__end_exam()


    def __go_next_question(self):
        self.screen_manager.change_sub_screen(self.questions[self.current_question])


    def __store_exam_results(self, scores, mistakes, time_seconds):
        json_manager = JsonManager()
        question_names = [question.get_game_name() for question in self.questions]
        json_manager.add_exam_completion(self.lesson_name, scores, mistakes, time_seconds, question_names)


    def __show_exam_results(self, scores, mistakes, time_seconds):
        screen = ResultsExamScreen(self.screen_name, self.screen_manager, mistakes, scores, time_seconds)
        self.screen_manager.change_sub_screen(screen)


    def __end_exam(self):
        time_seconds = time.time() - self.start_time
        mistakes = [screen.get_num_mistakes() for screen in self.questions]
        scores = self.__compute_exam_scores()
        self.__store_exam_results(scores, mistakes, time_seconds)
        self.__show_exam_results(scores, mistakes, time_seconds)
        

    def __is_sign_detection_question(self, question):
        return question == SignDetectionScreen


    def __compute_exam_scores(self):
        scores = []
        for question in self.questions:
            num_mistakes = question.get_num_mistakes()
            if self.__is_sign_detection_question(question):
                penalization = min(1, num_mistakes * penalization_sign)
            else:
                penalization = min(1, num_mistakes * penalization_game)
            scores.append(1 - penalization)
        return scores


    def __select_questions_randomly(self, num_questions, available_questions):
        return self.rng.choice(available_questions, num_questions)