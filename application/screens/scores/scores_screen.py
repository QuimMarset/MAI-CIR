from datetime import timedelta
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from application.screens.basic_screen import BasicScreen
from application.database.json_manager import JsonManager
from application.application_utils import crete_markup_text
from constants import red_color_str, green_color_str, medium_font_size, maroon_color_str



class ScoresScreen(BasicScreen):

    def __init__(self, screen_name, screen_manager, lesson_name, **kwargs):
        super().__init__(screen_name, screen_manager, **kwargs)
        self.lesson_name = lesson_name
        self.__build_screen()

    
    def __build_screen(self):
        json_manager = JsonManager()
        data = json_manager.read()
        lesson_data = data[self.lesson_name]

        anchor_layout = AnchorLayout()
        self.box_layout = BoxLayout(orientation='vertical', size_hint_y=0.7)
        anchor_layout.add_widget(self.box_layout)
        self.add_widget(anchor_layout)

        self.__print_completed(lesson_data)
        self.__print_lesson_time(lesson_data)
        self.__print_exam_results(lesson_data)
        self.__print_games_results(lesson_data)


    def __print_completed(self, lesson_data):
        completed = lesson_data['Completed']
        text_color = green_color_str if completed else red_color_str
        text = 'Completed' if completed else 'Not Completed'
        text = crete_markup_text(text, medium_font_size, text_color)
        label = Label(markup=True, text=text)
        self.box_layout.add_widget(label)


    def __format_time(self, time_seconds):
        time_str = str(timedelta(seconds=time_seconds))
        split = time_str.split(':')
        seconds = split[2].split('.')[0]
        time_str = split[0] + ':' + split[1] + ':' + seconds
        return time_str


    def __print_lesson_time(self, lesson_data):
        time_seconds = lesson_data['Time']
        time_str = self.__format_time(time_seconds)
        text = crete_markup_text('Total Time:   ', medium_font_size, maroon_color_str)
        text += crete_markup_text(time_str, medium_font_size, maroon_color_str)
        label = Label(markup=True, text=text)
        self.box_layout.add_widget(label)


    def __create_exam_label_text_score(self, text, exam_data):
        score = sum(exam_data['Scores'])
        score_color = green_color_str if score >= 5 else red_color_str
        text += crete_markup_text('Score: ', medium_font_size, maroon_color_str)
        text += crete_markup_text(str(score), medium_font_size, score_color)
        return text

    
    def __create_exam_label_text_time(self, text, exam_data):
        time_seconds = exam_data['Time']
        time_str = self.__format_time(time_seconds)
        text += crete_markup_text('  Time: ', medium_font_size, maroon_color_str)
        text += crete_markup_text(time_str, medium_font_size, maroon_color_str)
        return text


    def __create_exam_label_text(self, lesson_data):
        text = crete_markup_text('Exam:   ', medium_font_size, maroon_color_str)
        exam_data = lesson_data['Exam']
        if exam_data:
            text = self.__create_exam_label_text_score(text, exam_data)
            text = self.__create_exam_label_text_time(text, exam_data)
        else:
            text += crete_markup_text('Pending to do', medium_font_size, maroon_color_str)
        return text


    def __print_exam_results(self, lesson_data):
        text = self.__create_exam_label_text(lesson_data)
        label = Label(markup=True, text=text)
        self.box_layout.add_widget(label)


    def __search_best_try(self, games_data):
        best_index = -1
        min_errors = 0
        min_time = 0

        for i, try_data in enumerate(games_data):
            num_errors = sum(try_data['Mistakes'])
            time = try_data['Time']

            if best_index == -1 or num_errors < min_errors:
                best_index = i
                min_errors = num_errors
                min_time = time
            elif num_errors == min_errors and time < min_time:
                best_index = i
                min_time = time

        return best_index
        

    def __create_games_label_text_errors(self, text, best_try_data):
        errors = sum(best_try_data['Mistakes'])
        score_color = green_color_str if errors == 0 else red_color_str
        text += crete_markup_text('Errors: ', medium_font_size, maroon_color_str)
        text += crete_markup_text(str(errors), medium_font_size, score_color)
        return text


    def __create_games_label_text_time(self, text, best_try_data):
        time_seconds = best_try_data['Time']
        time_str = self.__format_time(time_seconds)
        text += crete_markup_text('  Time: ', medium_font_size, maroon_color_str)
        text += crete_markup_text(time_str, medium_font_size, maroon_color_str)
        return text


    def __create_games_label_text(self, games_data, best_index):
        text = crete_markup_text('Games Best Try:   ', medium_font_size, maroon_color_str)
        if best_index != -1:
            best_try_data = games_data[best_index]
            text = self.__create_games_label_text_errors(text, best_try_data)
            text = self.__create_games_label_text_time(text, best_try_data)
        else:
            text += crete_markup_text('No tries done', medium_font_size, maroon_color_str)
        return text
        

    def __print_games_results(self, lesson_data):
        games_data = lesson_data['Games']
        best_index = self.__search_best_try(games_data)
        text = self.__create_games_label_text(games_data, best_index)
        label = Label(markup=True, text=text)
        self.box_layout.add_widget(label)
