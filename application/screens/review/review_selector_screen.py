from os.path import join
from os import listdir
from application.screens.basic_screen import BasicScreen
from application.widgets.image_label_button import ImageLabelButton
from application.screens.review.review_screen import ReviewScreen
from constants import (icons_path, numbers_videos_path, letters_videos_path, 
    words_videos_path, number_type, word_type, letter_type)
from application.application_utils import create_grid_layout


class ReviewSelectorScreen(BasicScreen):

    def __init__(self, screen_manager, **kwargs):
        super().__init__('Review Screen', screen_manager, **kwargs)
        self.__build_screen()


    def __build_screen(self):
        self.grid_layout = create_grid_layout(cols=4, size_hint=(1, 0.5))

        self.button_review_numbers = ImageLabelButton(image_source=join(icons_path, 'lesson2.png'), text='Numbers', size_hint_x=0.45)
        self.button_review_letters = ImageLabelButton(image_source=join(icons_path, 'lesson2.png'), text='Letters', size_hint_x=0.45)
        self.button_review_words = ImageLabelButton(image_source=join(icons_path, 'lesson2.png'), text='Words', size_hint_x=0.45)

        self.button_review_numbers.bind(on_press=self.review_numbers_button_press)
        self.button_review_letters.bind(on_press=self.review_letters_button_press)
        self.button_review_words.bind(on_press=self.review_words_button_press)

        self.grid_layout.add_widget(self.button_review_numbers)
        self.grid_layout.add_widget(self.button_review_letters)
        self.grid_layout.add_widget(self.button_review_words)
        self.layout.add_widget(self.grid_layout)


    def review_numbers_button_press(self, *args):
        sign_visual_dict = self.create_sign_video_path_dict(numbers_videos_path)
        screen = ReviewScreen('Review Numbers Screen', self.screen_manager, sign_visual_dict)
        self.screen_manager.go_to_next_screen(screen)


    def review_letters_button_press(self, *args):
        sign_visual_dict = self.create_sign_video_path_dict(letters_videos_path)
        screen = ReviewScreen('Review Letters Screen', self.screen_manager, sign_visual_dict)
        self.screen_manager.go_to_next_screen(screen)


    def review_words_button_press(self, *args):
        sign_visual_dict = self.create_sign_video_path_dict(words_videos_path)
        screen = ReviewScreen('Review Words Screen', self.screen_manager, sign_visual_dict)
        self.screen_manager.go_to_next_screen(screen)


    def create_sign_video_path_dict(self, path):
        videos = listdir(path)
        sign_path_dict = {}
        for video in videos:
            sign_name = video.split('.')[0]
            video_path = join(path, video)
            sign_path_dict[sign_name] = video_path
        return sign_path_dict
