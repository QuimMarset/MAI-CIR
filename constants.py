import os
from os.path import join

# ===========
# Colors
# ===========

# Screen background color
light_green_color = [0.56, 0.72, 0.66, 1]
# Button color
cream_color = [0.98, 0.81, 0.73, 1.0]
# Text, border, action bar color
maroon_color = [0.46, 0.36, 0.41, 1]
# Wrong answer color
red_color = [1, 0, 0, 1]
# Correct answer color
green_color = [0.28, 0.63, 0.27, 1]
white_color = [1, 1, 1, 1]
red_pink_color = [0.94, 0.51, 0.55, 1]

maroon_color_str = '765D69'
red_pink_color_str = 'F1828D'
light_green_color_str = '8FB9A8'
red_color_str = 'FF0000'
green_color_str = '47A245'

# ===========
# Font sizes
# ===========

small_font_size = 15
medium_font_size = 20
big_font_size = 25

# ===========
# Others
# ===========

border_width = 2
pre_recording_time = 3
recording_time = 2

camera_resoulution = [640, 480]
camera_index = 0

# ===========
# Paths
# ===========

root_path = './'

application_path = join(root_path, 'application')
detectors_path = join(root_path, 'detectors')

kv_files_path = join(application_path, 'kv_files')
icons_path = join(application_path, 'icons')
videos_path = join('videos_and_images')
gifs_path = join('gifs')

numbers_videos_path = join(videos_path, 'numbers')
letters_videos_path = join(videos_path, 'letters')
words_videos_path = join(videos_path, 'words')
prediction_videos_path = join(videos_path, 'predictions')

numbers_gifs_path = join(gifs_path, 'numbers')
letters_gifs_path = join(gifs_path, 'letters')
words_gifs_path = join(gifs_path, 'words')

letters_detector_path = join(detectors_path, 'alphabet')
numbers_detector_path = join(detectors_path, 'numbers')
words_detector_path = join(detectors_path, 'words')

letters_model_path = join(letters_detector_path, 'MiCT-RANet34.pth')
numbers_model_path = join(numbers_detector_path, 'model_checkpoint.pth')
words_model_path = join(words_detector_path, 'spoter-checkpoint.pth')

numbers_model_config_path = join(numbers_detector_path, 'train_config.yaml')

gap_filling_words_path = join(application_path, 'screens', 'games', 'words.txt')

# ===========
# Sign Types
# ===========

number_type = 'numbers'
letter_type = 'letters'
word_type = 'words'

# ===========
# Lessons
# ===========

lessons_sign_types = [number_type, letter_type, letter_type, word_type]

lessons_names = ['Numbers 0-9', 'Vowels', 'Consonants B-J', 'Words 1']

lessons_signs = [
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['a', 'e', 'i', 'o', 'u'],
    ['b', 'c', 'd', 'f', 'g', 'h', 'j'],
    ['chair', 'dog', 'computer', 'book', 'drink', 'help', 'eat']
]

games_per_lesson = 7
num_multi_choice_options = 4
num_memory_pairs = 4
num_max_removed_letters = 2

num_exam_questions = 10
num_max_questions_detection = 1
seed = 42

penalization_sign = 0.15
penalization_game = 0.25