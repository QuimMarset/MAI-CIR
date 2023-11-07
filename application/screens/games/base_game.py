import numpy as np
from application.screens.basic_screen import BasicScreen




class BaseGame(BasicScreen):

    def __init__(self, screen_name, sign_visual_dict, parent_function, rng, game_name, **kwargs):
        super().__init__(screen_name, None, **kwargs)

        self.sign_visual_dict = sign_visual_dict
        self.parent_function = parent_function
        self.num_mistakes = 0
        self.game_name = game_name
        
        if rng is None:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng


    def finish_game(self):
        self.parent_function()

    
    def get_num_mistakes(self):
        return self.num_mistakes


    def get_game_name(self):
        return self.game_name