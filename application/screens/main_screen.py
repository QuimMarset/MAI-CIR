from os.path import join
from application.widgets.image_label_button import ImageLabelButton
from application.screens.basic_screen import BasicScreen
from application.screens.lessons.lessons_screen import LessonsScreen
from application.screens.review.review_selector_screen import ReviewSelectorScreen 
from application.screens.scores.scores_selector_screen import ScoresSelectorScreen
from application.application_utils import create_grid_layout
from constants import icons_path


class MainScreen(BasicScreen):

    def __init__(self, screen_manager, **kwargs):
        super().__init__('Main Screen', screen_manager, **kwargs)
        self.__build_screen()


    def __build_screen(self):
        self.grid_layout = create_grid_layout(cols=3, size_hint=(1, 0.5))
        
        self.button_learn = ImageLabelButton(image_source=join(icons_path, 'lesson.png'), text='Lessons', 
            on_press=self.lessons_button_press)
        
        #self.button_review = ImageLabelButton(image_source=join(icons_path, 'review.png'), text='Videos', 
        #    on_press=self.review_button_press)

        self.button_score = ImageLabelButton(image_source=join(icons_path, 'score.png'), text='Scores',
            on_press = self.score_button_press)

        self.grid_layout.add_widget(self.button_learn)
        #self.grid_layout.add_widget(self.button_review)
        self.grid_layout.add_widget(self.button_score)
        self.layout.add_widget(self.grid_layout)


    def lessons_button_press(self, *args):
        lessons_screen = LessonsScreen(self.screen_manager)
        self.screen_manager.go_to_next_screen(lessons_screen)

    
    def review_button_press(self, *args):
        review_selector_screen = ReviewSelectorScreen(self.screen_manager)
        self.screen_manager.go_to_next_screen(review_selector_screen)


    def score_button_press(self, *args):
        review_score_screen = ScoresSelectorScreen(self.screen_manager)
        self.screen_manager.go_to_next_screen(review_score_screen)
