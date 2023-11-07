from functools import partial
from kivy.clock import Clock
from constants import red_color, green_color, maroon_color, num_multi_choice_options
from application.screens.games.base_game import BaseGame
from application.widgets.image_button import ImageButton
from application.application_utils import create_grid_layout, create_label



class MultiChoiceInverseGameScreen(BaseGame):

    def __init__(self, screen_name, sign_visual_dict, parent_function, rng=None, **kwargs):
        super().__init__(screen_name, sign_visual_dict, parent_function, rng, 'MultiChoiceInverse', **kwargs)
        self.visual_sign_dict = dict(zip(sign_visual_dict.values(), sign_visual_dict.keys()))
        self.__create_question()
        self.__build_screen()


    def __create_question(self):
        visuals = list(self.visual_sign_dict.keys())
        self.correct_visual = self.rng.choice(visuals)
        visuals.remove(self.correct_visual)
        self.options = self.rng.choice(visuals, num_multi_choice_options-1, replace=False).tolist()
        self.options.append(self.correct_visual)
        self.rng.shuffle(self.options)


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=2, size_hint=(1, 0.8))
        self.layout.add_widget(self.grid_layout)

        text = f'Select the image/video corresponding to: {self.visual_sign_dict[self.correct_visual]}'
        label = create_label(text=text, size_hint=(1, 0.2))
        self.grid_layout.add_widget(label)

        self.grid_layout_options = create_grid_layout(cols=num_multi_choice_options, size_hint=(1, 0.7), 
            spacing='7dp')
        self.grid_layout.add_widget(self.grid_layout_options)

        for image_path in self.options:
            self.__add_image_button(image_path)

    
    def __add_image_button(self, visual_path):
        button = ImageButton(on_press=self.button_callback, image_source=visual_path, size_hint_y=0.4)
        button.id = visual_path
        self.grid_layout_options.add_widget(button)


    def button_callback(self, instance):
        if self.__correct_answer(instance.id):
            self.__trigger_color_change(instance, green_color)
            self.finish_game()
        else:
            self.num_mistakes += 1
            self.__trigger_color_change(instance, red_color)


    def __correct_answer(self, selected_sign):
        return selected_sign == self.correct_visual


    def set_match_color_to_default(self, button_pressed, *args):
        button_pressed.border_color = maroon_color


    def __trigger_color_change(self, button_pressed, color):
        button_pressed.border_color = color
        partial_func = partial(self.set_match_color_to_default, button_pressed)
        Clock.schedule_once(partial_func, 0.2)