from functools import partial
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from constants import green_color, red_color, maroon_color
from application.application_utils import create_grid_layout, create_label
from application.screens.games.base_game import BaseGame
from application.widgets.image_button import ImageButton



class NumberGapFillingGameScreen(BaseGame):

    def __init__(self, screen_name, sign_visual_dict, parent_function, rng=None, **kwargs):
        super().__init__(screen_name, sign_visual_dict, parent_function, rng, 'NumberGapFilling', **kwargs)
        self.current_index = 0
        self.__create_question()
        self.__build_screen()


    def __create_question(self):
        self.first_operand = self.rng.integers(0, 10)
        self.second_operand = self.rng.integers(1, 10)
        self.result = str(self.first_operand * self.second_operand)
        self.hidden_word = ' '.join(['_'] * len(self.result))


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=2, spacing='5dp')
        self.layout.add_widget(self.grid_layout)
        self.__build_instructions()
        self.__build_buttons()


    def __build_instructions(self):
        self.grid_layout_text = create_grid_layout(rows=2, size_hint=(1, 0.1))
        self.grid_layout.add_widget(self.grid_layout_text)

        instructions = ('Select the signs in the correct order to complete the ' +
            f'result of: {self.first_operand} x {self.second_operand}')
        instructions_label = create_label(text=instructions, size_hint=(1, 0.4))
        self.grid_layout_text.add_widget(instructions_label)

        self.word_label = create_label(text=self.hidden_word, size_hint=(1, 0.6))
        self.grid_layout_text.add_widget(self.word_label)


    def __build_buttons(self):
        anchor_layout = AnchorLayout()
        self.grid_layout.add_widget(anchor_layout)
       
        self.grid_layout_signs = create_grid_layout(rows=2, spacing='7dp',
            cols=len(self.sign_visual_dict) // 2, size_hint=(1, 0.9))
        anchor_layout.add_widget(self.grid_layout_signs)
        
        options = list(self.sign_visual_dict.keys())
        self.rng.shuffle(options)
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
        return selected_sign == self.result[self.current_index]


    def __update_hidden_word(self):
        index = 2 * self.current_index
        self.hidden_word = self.hidden_word[:index] + self.result[self.current_index] + self.hidden_word[index+1:]
        self.word_label.text = self.hidden_word
        self.current_index += 1


    def set_match_color_to_default(self, button_pressed, *args):
        button_pressed.border_color = maroon_color


    def __trigger_color_change(self, button_pressed, color):
        button_pressed.border_color = color
        partial_func = partial(self.set_match_color_to_default, button_pressed)
        Clock.schedule_once(partial_func, 0.2)


    def __is_game_finished(self):
        return self.current_index >= len(self.result)