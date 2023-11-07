import json
import pandas as pd
import os


lesson_names = [
    'Numbers 0-9',
    'Vowels',
    'Consonants B-J',
    'Words 1'
]


def read_database(json_path):
    with open(json_path, 'r', encoding='utf8') as file:
        dict = json.load(file)
    return dict


def get_lesson_exam_time(data, lesson_name):
    time = data[lesson_name]['Exam']['Time']
    return round(time, 2)


def get_lesson_exam_score(data, lesson_name):
    scores = data[lesson_name]['Exam']['Scores']
    return sum(scores)


def get_lesson_time(data, lesson_name):
    time = data[lesson_name]['Time']
    return round(time, 2)


def get_exams_times(data):
    times = []
    for lesson_name in lesson_names:
        time = get_lesson_exam_time(data, lesson_name)
        times.append(time)
    return times


def get_exams_scores(data):
    scores = []
    for lesson_name in lesson_names:
        score = get_lesson_exam_score(data, lesson_name)
        scores.append(score)
    return scores


def get_lessons_time(data):
    times = []
    for lesson_name in lesson_names:
        time = get_lesson_time(data, lesson_name)
        times.append(time)
    return times


def get_group_database_data(jsons_path):
    files = os.listdir(jsons_path)
    data = []

    for file in files:
        path = os.path.join(jsons_path, file)
        user_data = read_database(path)

        user_dict = {
            'lessons_times' : get_lessons_time(user_data),
            'exams_scores' : get_exams_scores(user_data),
            'exams_times' : get_exams_times(user_data)
        }

        data.append(user_dict)

    return pd.DataFrame(data)


def get_app_database_data(jsons_base_path):
    app_jsons_path = os.path.join(jsons_base_path, 'app')
    return get_group_database_data(app_jsons_path)


def get_videos_database_data(jsons_base_path):
    videos_jsons_path = os.path.join(jsons_base_path, 'videos')
    return get_group_database_data(videos_jsons_path)


def get_survey_scores(csv_path):
    data = pd.read_csv(csv_path)
    # Drop time column
    data.drop('Marca temporal', axis=1, inplace=True)

    # Change the polarity such that bigger values mean more difficult
    data['Q2'] = 5 - data['Q2'] + 1
    data['Q5'] = 5 - data['Q5'] + 1

    return data