import json
import os


FILENAME = "application\database\db_json.json"

class JsonManager:
    
    def __init__(self):
        self.filename = FILENAME
        self.create_file_if_not_exists()


    def create_file_if_not_exists(self):
        if os.path.exists(self.filename):
            return
        else:
            self.write({'Running_Time' : 0})


    def read(self):
        with open(self.filename, 'r') as file:
            return json.load(file)


    def write(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)


    def create_lesson(self, lesson_name):
        data = self.read()
        if lesson_name in data:
            return
        data[lesson_name] = {
            'Theory' : 0,
            'Practise' : 0,
            'Games' : [],
            'Exam' : {},
            'Time' : 0,
            'Completed' : False
        }
        self.write(data)


    def create_lessons(self, lesson_names):
        for lesson_name in lesson_names:
            self.create_lesson(lesson_name)


    def add_theory_time(self, lesson_name, time_seconds):
        data = self.read()
        data[lesson_name]['Theory'] += round(time_seconds, 3)
        data[lesson_name]['Time'] += round(time_seconds, 3)
        self.write(data)

    
    def add_practise_time(self, lesson_name, time_seconds):
        data = self.read()
        data[lesson_name]['Practise'] += round(time_seconds, 3)
        data[lesson_name]['Time'] += round(time_seconds, 3)
        self.write(data)


    def add_games_try(self, lesson_name, game_names, mistakes, time_seconds):
        data = self.read()
        tries = data[lesson_name]['Games']
        tries.append(
            {
                'Sequence' : game_names,
                'Mistakes' : mistakes,
                'Time' : round(time_seconds, 3)
            }
        )
        data[lesson_name]['Time'] += round(time_seconds, 3)
        self.write(data)

    
    def add_exam_completion(self, lesson_name, scores, mistakes, time_seconds, question_names):
        data = self.read()
        exam = data[lesson_name]['Exam']
        exam['Scores'] = scores
        exam['Mistakes'] = mistakes
        exam['Names'] = question_names
        exam['Time'] = round(time_seconds, 3)
        data[lesson_name]['Time'] += round(time_seconds, 3)
        data[lesson_name]['Completed'] = True
        self.write(data)


    def is_lesson_completed(self, lesson_name):
        data = self.read()
        return data[lesson_name]['Completed']


    def add_execution_time(self, time_seconds):
        data = self.read()
        data['Running_Time'] += round(time_seconds, 3)
        self.write(data)
