import pingouin as pg
from scipy import stats
from itertools import chain, combinations
import numpy as np


lesson_weights = [0.2, 0.25, 0.25, 0.3]

def compute_lesson_mean_value(exam_values):
    mean = 0
    for value, weight in zip(exam_values, lesson_weights):
        mean += value * weight
    return mean


def compute_exam_mean_score(exam_scores):
    return compute_lesson_mean_value(exam_scores)


def compute_exam_mean_time(exam_times):
    return compute_lesson_mean_value(exam_times)


def compute_lesson_mean_time(lesson_times):
    return compute_lesson_mean_value(lesson_times)


def compute_mean_scores(dataframe):
    for index, row in dataframe.iterrows():
        dataframe.at[index, 'mean_exam_score'] = compute_exam_mean_score(row['exams_scores'])
        dataframe.at[index, 'mean_exam_time'] = compute_exam_mean_time(row['exams_times'])
        dataframe.at[index, 'mean_lesson_time'] = compute_lesson_mean_time(row['lessons_times'])


def compute_mann_whitney_test(app_values, video_values, alternative='two-sided'):
    _, p_value = stats.mannwhitneyu(app_values, video_values, alternative=alternative)
    return p_value


def compute_t_test(app_values, video_values, alternative='two-sided'):
    _, p_value = stats.ttest_ind(app_values, video_values, alternative=alternative)
    return p_value


def get_best_subset_of_questions(dataframe):
    column_names = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    subsets = chain.from_iterable(combinations(column_names, size) 
        for size in range(2, 6))

    best_subset = None
    max_value = 0

    for subset in subsets:
        subset = list(subset)
        value, _ = pg.cronbach_alpha(dataframe[subset])
        #print(subset, value)
        if value > max_value:
            best_subset = subset
            max_value = value

    if best_subset:
        print(f'Best Cronbach Alpha obtained when using {best_subset} columns: {max_value}')
    return best_subset


def compute_questions_mean(dataframe):
    for index, row in dataframe.iterrows():
        mean_value = row.mean()
        dataframe.at[index, 'mean_value'] = mean_value


def compute_saphiro_wilk_test(dataframe):
    _, p_value = stats.shapiro(dataframe)
    return p_value