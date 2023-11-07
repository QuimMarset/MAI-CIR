import numpy as np
import time
from application.widgets.continue_popup import ContinuePopup
from application.screens.results.results_games_screen import ResultsGamesScreen
from application.screens.games.games_utils import *
from application.database.json_manager import JsonManager
from constants import games_per_lesson


class GamesSequence:

    def __init__(self, screen_name, screen_manager, lesson_name, sign_visual_dict, sign_type, **kwargs):
        self.screen_manager = screen_manager
        self.screen_name = screen_name
        self.lesson_name = lesson_name
        self.sign_visual_dict = sign_visual_dict
        self.sign_type = sign_type
        self.current_game = 0
        self.current_game_name = ""
        self.start_time = time.time()
        self.__create_game_sequence()


    def __create_game_sequence(self):
        self.games_screens = []
        games_classes = self.__select_games_randomly()
        for game_class in games_classes:
            game_screen = game_class(self.screen_name, self.sign_visual_dict, self.create_popup)
            self.games_screens.append(game_screen)


    def create_popup(self):
        ContinuePopup(self.advance_sequence).open()


    def go_first_game(self):
        self.current_game_name = self.games_screens[self.current_game].get_game_name()
        self.time_game_init = time.time()
        self.screen_manager.change_sub_screen(self.games_screens[self.current_game], save=True)


    def advance_sequence(self):
        self.current_game += 1
        if self.current_game < games_per_lesson:
            self.__go_next_game()
        else:
            self.__end_game_sequence()


    def __go_next_game(self):
        self.current_game_name = self.games_screens[self.current_game].get_game_name()
        self.time_game_init = time.time()
        self.screen_manager.change_sub_screen(self.games_screens[self.current_game])


    def __show_results(self, num_mistakes, time_seconds):
        screen = ResultsGamesScreen(self.screen_name, self.screen_manager, num_mistakes, time_seconds)
        self.screen_manager.change_sub_screen(screen)


    def __store_sequence_results(self, mistakes, time_seconds):
        json_manager = JsonManager()
        game_names = [game.get_game_name() for game in self.games_screens]
        json_manager.add_games_try(self.lesson_name, game_names, mistakes, time_seconds)


    def __end_game_sequence(self):
        mistakes = [screen.get_num_mistakes() for screen in self.games_screens]
        time_seconds = time.time() - self.start_time
        self.__store_sequence_results(mistakes, time_seconds)
        self.__show_results(sum(mistakes), time_seconds)
        

    def __select_games_randomly(self):
        available_games = get_available_games(self.sign_type)
        return np.random.choice(available_games, games_per_lesson)