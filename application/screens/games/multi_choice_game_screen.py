from functools import partial
from kivy.clock import Clock
from kivy.uix.image import Image
from constants import *
from application.screens.games.base_game import BaseGame
from application.widgets.custom_button import CustomButton
from constants import maroon_color, green_color, red_color, num_multi_choice_options
from application.application_utils import create_grid_layout, create_label



class MultiChoiceGameScreen(BaseGame):

    def __init__(self, screen_name, sign_visual_dict, parent_function, rng=None, **kwargs):
        super().__init__(screen_name, sign_visual_dict, parent_function, rng, 'MultiChoice', **kwargs)
        self.__create_question()
        self.__build_screen()


    def __create_question(self):
        sign_names = list(self.sign_visual_dict.keys())
        self.correct_sign = self.rng.choice(sign_names)
        sign_names.remove(self.correct_sign)
        self.options = self.rng.choice(sign_names, num_multi_choice_options-1, replace=False).tolist()
        self.options.append(self.correct_sign)
        self.rng.shuffle(self.options)


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=3, size_hint=(1, 0.8))
        self.layout.add_widget(self.grid_layout)

        instructions = 'Select the sign you see in the image/video'
        label = create_label(text=instructions, size_hint=(1, 0.1))
        self.grid_layout.add_widget(label)

        image = Image(source=self.sign_visual_dict[self.correct_sign], size_hint=(0.8, 0.6), anim_delay=1/25)
        self.grid_layout.add_widget(image)

        self.grid_layout_options = create_grid_layout(cols=num_multi_choice_options, size_hint=(0.8, 0.3))
        self.grid_layout.add_widget(self.grid_layout_options)

        for name in self.options:
            self.__add_button(name)

    
    def __add_button(self, sign_name):
        button = CustomButton(text=sign_name, on_press=self.button_callback, size_hint_y=0.8)
        button.id = sign_name
        self.grid_layout_options.add_widget(button)


    def button_callback(self, instance):
        if self.__correct_answer(instance.id):
            self.__trigger_color_change(instance, green_color)
            self.finish_game()
        else:
            self.num_mistakes += 1
            self.__trigger_color_change(instance, red_color)


    def __correct_answer(self, selected_sign):
        return selected_sign == self.correct_sign


    def set_match_color_to_default(self, button_pressed, *args):
        button_pressed.border_color = maroon_color


    def __trigger_color_change(self, button_pressed, color):
        button_pressed.border_color = color
        partial_func = partial(self.set_match_color_to_default, button_pressed)
        Clock.schedule_once(partial_func, 0.2)
    