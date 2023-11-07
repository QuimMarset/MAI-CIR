import random
from functools import partial
from collections import Counter
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from constants import red_color, green_color, maroon_color, gap_filling_words_path, num_max_removed_letters
from application.application_utils import create_grid_layout, create_label
from application.screens.games.base_game import BaseGame
from application.widgets.image_button import ImageButton



class WordGapFillingGameScreen(BaseGame):

    def __init__(self, name, sign_visual_dict, parent_function, rng=None, **kwargs):
        super().__init__(name, sign_visual_dict, parent_function, rng, 'WordGapFilling', **kwargs)
        self.current_index = 0
        self.__choose_word()
        self.__create_question()
        self.__build_screen()


    def __get_words_for_gap_filling(self):
        words = []
        with open(gap_filling_words_path, 'r') as file:
            for line in file.readlines():
                word = line.strip()
                words.append(word)
        return words


    def __filter_words(self, words):
        filtered_words = []
        for word in words:
            occurrences = Counter(word)
            num_interested_letters = sum([occurrences.get(letter, 0) for letter in self.sign_visual_dict])
            if num_interested_letters > 0:
                filtered_words.append(word)
        return filtered_words


    def __choose_word(self):
        words = self.__get_words_for_gap_filling()
        filtered_words = self.__filter_words(words)
        self.word = self.rng.choice(filtered_words)

    
    def __get_indices_of_letters(self):
        indices = []
        previous = -1
        for i, char in enumerate(self.word):
            if char in self.sign_visual_dict:
                if previous == -1 or previous != i-1:
                    indices.append(i)
                    previous = i
        return indices


    def __get_letters_to_hide(self):
        indices = self.__get_indices_of_letters()

        if len(indices) > num_max_removed_letters:
            num_to_remove = num_max_removed_letters
        elif len(self.word) < 5:
            num_to_remove = 1
        else:
            num_to_remove = len(indices)

        indices = self.rng.choice(indices, num_to_remove, replace=False)
        indices = sorted(indices)
        return indices


    def __create_question(self):
        self.indices = self.__get_letters_to_hide()
        hidden_word = []

        for i, char in enumerate(self.word):
            if i in self.indices:
                hidden_word.append('_')
            else:
                hidden_word.append(char)

        self.hidden_word = ' '.join(hidden_word)


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=2, spacing='15dp')
        self.layout.add_widget(self.grid_layout)
        self.__build_instructions()
        self.__build_buttons()


    def __build_instructions(self):
        self.grid_layout_text = create_grid_layout(rows=2, size_hint=(1, 0.1), spacing='30dp')
        self.grid_layout.add_widget(self.grid_layout_text)

        instructions = 'Select the signs in the correct order to complete the word:'
        instructions_label = create_label(text=instructions, size_hint=(1, 0.5))
        self.grid_layout_text.add_widget(instructions_label)

        self.word_label = create_label(text=self.hidden_word, size_hint=(1, 0.5))
        self.grid_layout_text.add_widget(self.word_label)

    
    def __compute_num_cols(self):
        num_cols = len(self.sign_visual_dict) // 2
        modulo = len(self.sign_visual_dict) % 2
        if modulo > 0:
            num_cols += 1
        return num_cols


    def __build_buttons(self):
        anchor_layout = AnchorLayout()
        self.grid_layout.add_widget(anchor_layout)

        num_cols = self.__compute_num_cols()
        self.grid_layout_signs = create_grid_layout(rows=2, cols=num_cols, 
            spacing='7dp', size_hint=(1, 0.9))
        anchor_layout.add_widget(self.grid_layout_signs)
        
        options = list(self.sign_visual_dict.keys())
        random.shuffle(options)
        for sign in options:
            self.__add_button(sign)

    
    def __add_button(self, sign):
        visual_path = self.sign_visual_dict[sign]
        button = ImageButton(on_press=self.button_callback, image_source=visual_path, size_hint_y=0.4)
        button.id = sign
        self.grid_layout_signs.add_widget(button)


    def button_callback(self, instance):
        if self.__correct_answer(instance.id):
            self.__trigger_color_change(instance, green_color)
            self.__update_hidden_word()
            if self.__is_game_finished():
                self.finish_game()
        else:
            self.num_mistakes += 1
            self.__trigger_color_change(instance, red_color)


    def __correct_answer(self, selected_sign):
        word_index = self.indices[self.current_index]
        return selected_sign == self.word[word_index]


    def __update_hidden_word(self):
        word_index = self.indices[self.current_index]
        index = 2 * word_index
        self.hidden_word = self.hidden_word[:index] + self.word[word_index] + self.hidden_word[index+1:]
        self.word_label.text = self.hidden_word
        self.current_index += 1


    def set_match_color_to_default(self, button_pressed, *args):
        button_pressed.border_color = maroon_color


    def __trigger_color_change(self, button_pressed, color):
        button_pressed.border_color = color
        partial_func = partial(self.set_match_color_to_default, button_pressed)
        Clock.schedule_once(partial_func, 0.2)


    def __is_game_finished(self):
        return self.current_index >= len(self.indices)