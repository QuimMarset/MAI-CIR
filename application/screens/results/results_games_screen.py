from datetime import timedelta
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from application.screens.basic_screen import BasicScreen
from application.widgets.custom_button import CustomButton
from application.application_utils import create_grid_layout, crete_markup_text, create_label
from constants import red_color_str, green_color_str, medium_font_size, maroon_color_str



class ResultsGamesScreen(BasicScreen):

    def __init__(self, name, screen_manager, num_mistakes, time_seconds, **kwargs):
        super().__init__(name, screen_manager, **kwargs)
        self.__build_screen(num_mistakes, time_seconds)


    def __build_screen(self, num_mistakes, time_seconds):
        self.grid_layout = create_grid_layout(rows=3, size_hint=(0.5, 1))
        self.layout.add_widget(self.grid_layout)
        self.__create_mistakes_label(num_mistakes)
        self.__create_time_label(time_seconds)
        self.__create_finish_button()


    def __create_mistakes_label(self, num_mistakes):
        text = crete_markup_text('Number of errors: ', medium_font_size, maroon_color_str)
        color = green_color_str if num_mistakes == 0 else red_color_str
        text += crete_markup_text(str(num_mistakes), medium_font_size, color)
        label = Label(markup=True, text=text)
        self.grid_layout.add_widget(label)


    def __create_time_label(self, time_seconds):
        time_str = str(timedelta(seconds=time_seconds))
        time_str = self.__format_time(time_str)
        text = 'Total time: ' +  time_str
        label = create_label(text=text)
        self.grid_layout.add_widget(label)

    
    def __format_time(self, time_str):
        split = time_str.split(':')
        seconds = split[2].split('.')[0]
        time_str = split[0] + ':' + split[1] + ':' + seconds
        return time_str


    def __create_finish_button(self):
        anchor_layout = AnchorLayout()
        self.grid_layout.add_widget(anchor_layout)
        anchor_layout.add_widget(CustomButton(text='Finish', size_hint=(1, 0.4), on_release=self.button_callback))


    def button_callback(self, *args):
        self.screen_manager.go_to_previous_screen()