from functools import partial
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from application.screens.games.base_game import BaseGame
from application.widgets.image_toggle_button import ImageToggleButton
from application.widgets.custom_toggle_button import CustomToggleButton
from application.application_utils import create_grid_layout, create_label
from constants import red_color, green_color, maroon_color, num_memory_pairs



class MemoryGameScreen(BaseGame):

    def __init__(self, screen_name, sign_visual_dict, parent_function, rng=None, **kwargs):
        super().__init__(screen_name, sign_visual_dict, parent_function, rng, 'MemoryGame', **kwargs)
        self.text_buttons = []
        self.image_buttons = []
        self.num_cleared = 0
        self.text_pressed = None
        self.image_pressed = None
        self.__select_signs_subset()
        self.__build_screen()


    def __select_signs_subset(self):
        sign_names = list(self.sign_visual_dict.keys())
        self.selected_signs = self.rng.choice(sign_names, num_memory_pairs, replace=False)


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=2)
        self.layout.add_widget(self.grid_layout)
        self.__create_instructions_label()
        self.__create_button_pairs()

    
    def __create_instructions_label(self):
        text = 'Pair each sign with its corresponding image/video'
        label = create_label(text=text, size_hint=(1, 0.1))
        self.grid_layout.add_widget(label)


    def __create_button_pairs(self):
        self.grid_layout_pairs = create_grid_layout(rows=len(self.selected_signs) // 2, cols=4, padding='5dp', spacing='7dp')
        self.grid_layout.add_widget(self.grid_layout_pairs)

        sign_names = [key for key in self.selected_signs]
        sign_visual_paths = [self.sign_visual_dict[key] for key in self.selected_signs]
        self.rng.shuffle(sign_names)
        self.rng.shuffle(sign_visual_paths)

        for name, visual_path in zip(sign_names, sign_visual_paths):
            self.__add_text_button(name)
            self.__add_image_button(visual_path)

    
    def __add_text_button(self, sign_name):
        anchor_layout = AnchorLayout()
        button = CustomToggleButton(text=sign_name, on_press=self.text_button_callback, size_hint=(0.8, 0.5))
        button.id = sign_name
        anchor_layout.add_widget(button)
        self.grid_layout_pairs.add_widget(anchor_layout)
        self.text_buttons.append(button)


    def __add_image_button(self, visual_path):
        button = ImageToggleButton(image_source=visual_path, on_press=self.image_button_callback)
        button.id = visual_path
        self.grid_layout_pairs.add_widget(button)
        self.image_buttons.append(button)


    def text_button_callback(self, instance):
        self.text_pressed = instance
        self.__common_button_callback(self.text_pressed, self.image_pressed, self.text_buttons)


    def image_button_callback(self, instance):
        self.image_pressed = instance
        self.__common_button_callback(self.image_pressed, self.text_pressed, self.image_buttons)


    def __common_button_callback(self, pressed_button, other_type_button, other_buttons):
        pressed_button.disabled = True
        self.__unselect_other_buttons(pressed_button, other_buttons)
        
        if other_type_button == None:
            return

        if self.__pair_matches():
            self.__correct_match_process()
        else:
            self.__incorrect_match_process()

        self.__forget_stored_buttons()

        if self.__is_game_finished():
            self.finish_game()

    
    def __unselect_other_buttons(self, current_pressed, buttons):
        for button in buttons:
            if button == current_pressed:
                continue
            button.disabled = False
            button.state = 'normal'


    def __pair_matches(self):
        sign_name = self.text_pressed.id
        image_path = self.image_pressed.id
        return self.sign_visual_dict[sign_name] == image_path


    def __correct_match_process(self):
        self.num_cleared += 1
        self.__remove_current_pair()
        self.__enable_all_buttons()
        self.__trigger_color_change(green_color)

    
    def __incorrect_match_process(self):
        self.num_mistakes += 1
        self.__enable_all_buttons()
        self.__unselect_current()
        self.__trigger_color_change(red_color)


    def __forget_stored_buttons(self):
        self.image_pressed = None
        self.text_pressed = None
        

    def __remove_current_pair(self):
        self.text_pressed.disabled = True
        self.image_pressed.disabled = True
        self.text_buttons.remove(self.text_pressed)
        self.image_buttons.remove(self.image_pressed)
            

    def __enable_all_buttons(self):
        for text_button, image_button in zip(self.text_buttons, self.image_buttons):
            text_button.disabled = False
            image_button.disabled = False


    def __unselect_current(self):
        self.text_pressed.state = 'normal'
        self.image_pressed.state = 'normal'


    def set_match_color_to_default(self, text_pressed, image_pressed, *args):
        text_pressed.border_color = maroon_color
        image_pressed.border_color = maroon_color


    def __trigger_color_change(self, color):
        self.text_pressed.border_color = color
        self.image_pressed.border_color = color
        partial_func = partial(self.set_match_color_to_default, self.text_pressed, self.image_pressed)
        Clock.schedule_once(partial_func, 0.2)


    def __is_game_finished(self):
        return self.num_cleared == len(self.selected_signs)