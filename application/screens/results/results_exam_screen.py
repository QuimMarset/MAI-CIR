from datetime import timedelta
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from application.screens.basic_screen import BasicScreen
from application.widgets.custom_button import CustomButton
from application.application_utils import create_grid_layout, crete_markup_text, create_label
from constants import red_color_str, green_color_str, medium_font_size, maroon_color_str



class ResultsExamScreen(BasicScreen):

    def __init__(self, name, screen_manager, mistakes, scores, time_seconds, **kwargs):
        super().__init__(name, screen_manager, **kwargs)
        self.__build_screen(mistakes, scores, time_seconds)


    def __build_screen(self, mistakes, scores, time_seconds):
        num_rows = len(mistakes) + 3
        self.grid_layout = create_grid_layout(rows=num_rows, spacing='5dp')
        self.layout.add_widget(self.grid_layout)
        self.__create_scores_labels(mistakes, scores)
        self.__create_final_score_label(scores)
        self.__create_time_label(time_seconds)
        self.__create_finish_button()


    def __create_score_label_text(self, question_mistakes, score):
        mistakes_color = green_color_str if question_mistakes == 0 else red_color_str
        text = crete_markup_text('Number of errors: ', medium_font_size, maroon_color_str)
        mistakes = 'Omitted' if question_mistakes == 999 else str(question_mistakes)
        text += crete_markup_text(mistakes, medium_font_size, mistakes_color)
        text += crete_markup_text('    Score: ', medium_font_size, maroon_color_str)
        text += crete_markup_text(str(score), medium_font_size, maroon_color_str)
        return text


    def __create_scores_labels(self, mistakes, scores):
        for question_mistakes, score in zip(mistakes, scores):
            text = self.__create_score_label_text(question_mistakes, score)
            label = Label(markup=True, text=text)
            self.grid_layout.add_widget(label)


    def __create_final_score_label(self, scores):
        final_score = sum(scores)
        text = 'Test score: ' +  str(final_score)
        label = create_label(text=text)
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
        anchor_layout.add_widget(CustomButton(text='Finish', size_hint=(0.5, 0.8), 
            on_release=self.button_callback))


    def button_callback(self, *args):
        self.screen_manager.go_to_lesson_from_exam()