from os.path import join
from constants import (number_type, letter_type, word_type, 
    numbers_videos_path, numbers_gifs_path, letters_videos_path, letters_gifs_path,
    words_videos_path, words_gifs_path)



def get_correct_video_folder(sign_type):
    if sign_type == number_type:
        return numbers_videos_path
    elif sign_type == letter_type:
        return letters_videos_path
    elif sign_type == word_type:
        return words_videos_path
    else:
        raise ValueError(sign_type)


def get_correct_gif_folder(sign_type):
    if sign_type == number_type:
        return numbers_gifs_path
    elif sign_type == letter_type:
        return letters_gifs_path
    elif sign_type == word_type:
        return words_gifs_path
    else:
        raise ValueError(sign_type)


def create_paths_to_visuals(signs, folder, extension):
    paths = []
    for sign in signs:
        path = join(folder, f'{sign}.{extension}')
        paths.append(path)
    return paths


def get_signs_video_paths(signs, sign_type):
    video_folder = get_correct_video_folder(sign_type)
    video_paths = create_paths_to_visuals(signs, video_folder, 'mp4')
    return video_paths


def get_signs_gif_paths(signs, sign_type):
    gif_folder = get_correct_gif_folder(sign_type)
    gif_paths = create_paths_to_visuals(signs, gif_folder, 'zip')
    return gif_paths


def create_signs_video_paths_dict(signs, sign_type):
    video_paths = get_signs_video_paths(signs, sign_type)
    return dict(zip(signs, video_paths))


def create_signs_gif_paths_dict(signs, sign_type):
    gif_paths = get_signs_gif_paths(signs, sign_type)
    return dict(zip(signs, gif_paths))