import os
from extract_data import *
from generate_plots import *
from compute_statistics import *




if __name__ == '__main__':

    root_path = 'statistics'
    jsons_path = os.path.join(root_path, 'jsonfiles')

    results_path = os.path.join(root_path, 'results')
    os.makedirs(results_path, exist_ok=True)

    # Get data from the database for both groups
    app_data = get_app_database_data(jsons_path)
    videos_data = get_videos_database_data(jsons_path)

    # Generate boxplots of the different type of data we store in the database
    plot_boxplots(lesson_names, app_data['exams_scores'].tolist(), 
        videos_data['exams_scores'].tolist(), 'exams_scores', results_path)

    plot_boxplots(lesson_names, app_data['exams_times'].tolist(), 
        videos_data['exams_times'].tolist(), 'exams_times', results_path)

    plot_boxplots(lesson_names, app_data['lessons_times'].tolist(), 
        videos_data['lessons_times'].tolist(), 'lesson_times', results_path)

    # Compute the means using the 4 lessons of the exam scores, exam times, and lesson times
    compute_mean_scores(app_data)
    compute_mean_scores(videos_data)

    # Plot the distributions of the exam scores, exam times, and lesson times for each group
    plot_scores_distribution(app_data['mean_exam_score'].tolist(), 'exam scores', results_path, videos=False)
    plot_time_distribution(app_data['mean_exam_time'].tolist(), 'exam time', results_path, videos=False)
    plot_time_distribution(app_data['mean_lesson_time'].tolist(), 'lesson time', results_path, videos=False)

    plot_scores_distribution(videos_data['mean_exam_score'].tolist(), 'exam scores', results_path, videos=True)
    plot_time_distribution(videos_data['mean_exam_time'].tolist(), 'exam time', results_path, videos=True)
    plot_time_distribution(videos_data['mean_lesson_time'].tolist(), 'lesson time', results_path, videos=True)

    # Compute the Mann-Whitney U test to check if we can reject the null hypothesis of the learning progress
    p_value_score = compute_mann_whitney_test(app_data['mean_exam_score'].tolist(), videos_data['mean_exam_score'].tolist())
    p_value_exam_time = compute_mann_whitney_test(app_data['mean_exam_time'].tolist(), videos_data['mean_exam_time'].tolist())
    p_value_exam_lesson = compute_mann_whitney_test(app_data['mean_lesson_time'].tolist(), videos_data['mean_lesson_time'].tolist())

    print(f'Test the null hypothesis with the exam scores: p-value = {p_value_score:.2f} -> Reject? {p_value_score <= 0.05}')
    print(f'Test the null hypothesis with the exam times:  p-value = {p_value_exam_time:.2f} -> Reject? {p_value_exam_time <= 0.05}')
    print(f'Test the null hypothesis with the lesson times:  p-value = {p_value_exam_lesson:.2f} -> Reject? {p_value_exam_lesson <= 0.05}')

    # Get the data from the surveys
    surveys_path = os.path.join(root_path, 'surveys')
    survey_data_app = get_survey_scores(os.path.join(surveys_path, 'surveys_app.csv'))
    survey_data_videos = get_survey_scores(os.path.join(surveys_path, 'surveys_videos.csv'))
    
    # Use Cronbach's alpha to get the best subset of features (>= 0.7)
    survey_data = pd.concat([survey_data_app, survey_data_videos])
    survey_data.reset_index(inplace=True)
    best_subset = get_best_subset_of_questions(survey_data)
    survey_data_app = survey_data_app[best_subset]
    survey_data_videos = survey_data_videos[best_subset]

    # Generate boxplots for the subset of questions
    app_values = survey_data_app[best_subset].values.transpose().tolist()
    videos_values = survey_data_videos[best_subset].values.transpose().tolist()
    plot_boxplots_surveys(best_subset, app_values, videos_values, results_path)

    # Compute the composite score (a mean) of the best subset of questions for each user
    compute_questions_mean(survey_data_app)
    compute_questions_mean(survey_data_videos)

    # Plot the distribution to see which test to apply
    plot_survey_answer_distribution(survey_data_app['mean_value'].tolist(), results_path, videos=False)
    shapiro_p_value = compute_saphiro_wilk_test(survey_data_app)
    print(f'Does follow a normal distribution?: {shapiro_p_value > 0.05}')

    plot_survey_answer_distribution(survey_data_videos['mean_value'].tolist(), results_path, videos=True)
    shapiro_p_value = compute_saphiro_wilk_test(survey_data_videos)
    print(f'Does follow a normal distribution?: {shapiro_p_value > 0.05}')

    # Compute the Mann-Whitney U test to check if we can reject the null hypothesis of the learning satisfaction
    p_value_survey = compute_mann_whitney_test(survey_data_app['mean_value'].tolist(), 
        survey_data_videos['mean_value'].tolist(), alternative='less')
    print(f'Test the null hypothesis with the survey answers composite score: p-value = {p_value_survey:.2f} -> Reject? {p_value_survey <= 0.05}')
