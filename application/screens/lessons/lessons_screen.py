from os.path import join
from functools import partial
from application.widgets.image_label_button import ImageLabelButton
from application.screens.basic_screen import BasicScreen
from application.screens.lessons.lesson_screen import LessonScreen
from application.application_utils import create_grid_layout
from application.database.json_manager import JsonManager
from constants import icons_path, lessons_sign_types, lessons_names, lessons_signs


class LessonsScreen(BasicScreen):

    def __init__(self, screen_manager, **kwargs):
        super().__init__('Lessons Screen', screen_manager, **kwargs)
        self.num_lessons = len(lessons_sign_types)
        self.__build_screen()
        self.__create_lessons_in_database()


    def __build_screen(self):
        self.grid_layout = create_grid_layout(rows=2, cols=self.num_lessons // 2, size_hint=(0.8, 0.8))
        self.layout.add_widget(self.grid_layout)

        for i in range(self.num_lessons):
            screen_name = f'Lesson {i} - {lessons_names[i]}'
            sign_type = lessons_sign_types[i]
            lesson_signs = lessons_signs[i]
            partial_func = partial(self.button_callback, screen_name, lessons_names[i], sign_type, lesson_signs)

            lesson_button = ImageLabelButton(image_source=join(icons_path, 'lesson2.png'), text=screen_name)
            lesson_button.bind(on_press=partial_func)

            self.grid_layout.add_widget(lesson_button)


    def __create_lessons_in_database(self):
        json_manager = JsonManager()
        json_manager.create_lessons(lessons_names)


    def button_callback(self, screen_name, lesson_name, sign_type, lesson_signs_dict, *args):
        screen = LessonScreen(screen_name, self.screen_manager, lesson_name, sign_type, lesson_signs_dict)
        self.screen_manager.go_to_next_screen(screen)