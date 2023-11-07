from application.screens.games.memory_game_screen import MemoryGameScreen
from application.screens.games.multi_choice_game_screen import MultiChoiceGameScreen
from application.screens.games.multi_choice_inverse_game_screen import MultiChoiceInverseGameScreen
from application.screens.games.number_gap_filling_game_screen import NumberGapFillingGameScreen
from application.screens.games.word_gap_filling_game_screen import WordGapFillingGameScreen
from constants import number_type, word_type, letter_type



available_games = {
    number_type : [MemoryGameScreen, MultiChoiceGameScreen, MultiChoiceInverseGameScreen, NumberGapFillingGameScreen],
    letter_type : [MemoryGameScreen, MultiChoiceGameScreen, MultiChoiceInverseGameScreen, WordGapFillingGameScreen],
    word_type : [MemoryGameScreen, MultiChoiceGameScreen, MultiChoiceInverseGameScreen]
}


def get_available_games(sign_type):
    if sign_type == number_type:
        return available_games[number_type]
    elif sign_type == letter_type:
        return available_games[letter_type]
    elif sign_type == word_type:
        return available_games[word_type]
    else:
        raise ValueError(sign_type)