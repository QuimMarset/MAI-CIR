import seaborn as sns
from os.path import join
import matplotlib.pyplot as plt
import numpy as np


def get_lesson_names_for_boxplot(lesson_names):
    names = []
    for name in lesson_names:
        names.append(f'{name}\n App')
        names.append(f'{name}\n Videos')
    return names


def get_values_for_boxplot(app_values, videos_values):
    values = []
    for app_values_i, videos_values_i in zip(app_values, videos_values):
        values.append(app_values_i)
        values.append(videos_values_i)
    return values


def plot_boxplots(lesson_names, app_values, videos_values, data_type, save_path):
    sns.set(style='whitegrid')
    plt.figure(figsize=(12, 6))
    
    app_values = np.array(app_values).transpose().tolist()
    videos_values = np.array(videos_values).transpose().tolist()
    values = get_values_for_boxplot(app_values, videos_values)
    names = get_lesson_names_for_boxplot(lesson_names)
    
    plt.boxplot(values)
    
    ticks = range(1, len(names) + 1)
    plt.xticks(ticks, labels=names, fontsize=12)
    plt.xlabel('Lesson')

    if data_type == 'lesson_times':
        title = 'Time to complete each lesson in both groups'
        y_label = 'Time(s)'
    elif data_type == 'exams_times':
        title = 'Time to complete each exam in both groups'
        y_label = 'Time(s)'
    else:
        title = 'Score of each exam in both groups'
        y_label = 'Exam Score'

    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(join(save_path, f'lesson_boxplots_{data_type}.png'), dpi=150)


def plot_scores_distribution(values, data_type, save_path, videos=False):
    sns.set(style='whitegrid')
    plt.figure(figsize=(6, 6))
    plt.hist(values, bins=list(range(0, 11)))
    plt.xlabel('Mean value of the 4 lessons')
    plt.ylabel('Frequency')
    group = 'the application' if not videos else 'videos'
    plt.title(f'Distribution of {data_type} for those using {group}')
    plt.tight_layout()
    group = 'application' if not videos else 'videos'
    plt.savefig(join(save_path, f'mean_distribution_{data_type}_{group}'))


def plot_time_distribution(values, data_type, save_path, videos=False):
    sns.set(style='whitegrid')
    plt.figure(figsize=(6, 6))
    plt.hist(values, bins=5)
    plt.xlabel('Mean value of the 4 lessons')
    plt.ylabel('Frequency')
    group = 'the application' if not videos else 'videos'
    plt.title(f'Distribution of {data_type} for those using {group}')
    plt.tight_layout()
    group = 'application' if not videos else 'videos'
    plt.savefig(join(save_path, f'mean_distribution_{data_type}_{group}'))


def plot_survey_answer_distribution(values, save_path, videos=False):
    sns.set(style='whitegrid')
    plt.figure(figsize=(6, 6))
    plt.hist(values, bins=list(range(1, 6)))
    plt.xlabel('Mean value of the 4 lessons')
    plt.ylabel('Frequency')
    group = 'the application' if not videos else 'videos'
    plt.title(f'Distribution of the composite score of the survey for those using {group}')
    plt.tight_layout()
    group = 'application' if not videos else 'videos'
    plt.savefig(join(save_path, f'mean_distribution_questions_{group}'))


def plot_boxplots_surveys(question_names, app_values, videos_values, save_path):
    sns.set(style='whitegrid')
    plt.figure(figsize=(12, 6))
    
    values = get_values_for_boxplot(app_values, videos_values)
    names = get_lesson_names_for_boxplot(question_names)
    
    plt.boxplot(values)
    
    ticks = range(1, len(names) + 1)
    plt.xticks(ticks, labels=names, fontsize=12)
    plt.xlabel('Lesson')

    plt.ylabel('Questions scores')
    plt.title('Scores of the selected questions for the two groups')
    plt.tight_layout()
    plt.savefig(join(save_path, f'surveys_boxplots.png'), dpi=150)