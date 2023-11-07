import pandas as pd
import os
import json

path = 'application\database\jsonfiles'
path_csv = 'application\database\csv_files'

data_app = pd.DataFrame()
data_videos = pd.DataFrame()

def json_to_csv():

    for file in os.listdir(path):
        if file.endswith('.json') and "app" in file:
            # add data to data_app
            data = pd.read_json(path + '\\' + file)
            data.to_csv(path_csv + '\\' + file + '.csv')

        elif file.endswith('.json') and "video" in file:
            data = pd.read_json(path + '\\' + file)
            data.to_csv(path_csv + '\\' + file + '.csv')
            

def create_csv_exams():
    df_videos = pd.DataFrame(columns=['Numbers 0-9', 'Vowels', 'Consonants B-J', 'Words 1'])
    df_app = pd.DataFrame(columns=['Numbers 0-9', 'Vowels', 'Consonants B-J', 'Words 1'])
    for file in os.listdir(path):
        if file.endswith('.json') and "app" in file:
            with open(os.path.join(path,file)) as f:
                data = json.load(f)
            keys = list(data.keys())[1:] # the first key that is running time
            # create new row to dataframe
            results = []

            for key in keys:
                results.append(data[key]["Exam"]["Time"])
            # add row to dataframe
            df_app.loc[len(df_app)] = results
            

        elif file.endswith('.json') and "video" in file:
            with open(os.path.join(path,file)) as f:
                data = json.load(f)
            keys = list(data.keys())[1:]
            # create new row to dataframe
            results = []

            for key in keys:
                results.append(data[key]["Exam"]["Time"])
            # add row to dataframe
            df_videos.loc[len(df_videos)] = results
    
    df_app.to_csv(path_csv + '\\' + 'app_statistics.csv')
    df_videos.to_csv(path_csv + '\\' + 'videos_statistics.csv')

def statistics():
    df_app = pd.read_csv(path_csv + '\\' + 'app_statistics.csv')
    df_videos = pd.read_csv(path_csv + '\\' + 'videos_statistics.csv')
    df_app = df_app.drop(columns=['Unnamed: 0'])
    df_videos = df_videos.drop(columns=['Unnamed: 0'])
    df_app = df_app.mean()
    df_videos = df_videos.mean()
    # save as mean_app and mean_videos
    df_app.to_csv(path_csv + '\\' + 'mean_app.csv')
    df_videos.to_csv(path_csv + '\\' + 'mean_videos.csv')



if __name__ == "__main__":
    statistics()