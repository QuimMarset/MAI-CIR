import cv2
import time
from threading import Thread
from os import makedirs
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from application.screens.basic_screen import BasicScreen
from application.screens.sign_detection.sign_detection_utils import get_detection_method
from constants import *


# Abstract class (DO NOT INSTANTIATE IT)
class BaseSignDetectorScreen(BasicScreen):

    expected_sign = StringProperty('')
    predicted_sign = StringProperty('')
    instructions_text = StringProperty('')
    
    border_width = NumericProperty(border_width)
    border_color = ListProperty(maroon_color)
    text_color = ListProperty(maroon_color)
    button_color = ListProperty(cream_color)
    answer_color = ListProperty(maroon_color)

    small_font_size = NumericProperty(small_font_size)
    medium_font_size = NumericProperty(medium_font_size)


    def __init__(self, screen_name, screen_manager, sign_type, **kwargs):
        super().__init__(screen_name, screen_manager, **kwargs)
        self.sign_type = sign_type
        self.record_video = False
        self.start_recording_time = 0
        self.camera = self.ids.camera
        self.__bind_buttons_to_stop_camera()
        self.__set_video_capture()
        self.initialize_instructions()
        Clock.schedule_interval(self.update_frame, 1 / self.fps)

    
    def __create_video_path(self):
        makedirs(prediction_videos_path, exist_ok=True)
        self.file_name = join(prediction_videos_path, f'{self.expected_sign}_detection.mp4')


    def __set_video_capture(self):
        self.capture = cv2.VideoCapture(camera_index)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.video_type = cv2.VideoWriter_fourcc(*'DIVX')        
        

    def start_sign_detection_callback(self, *args):
        self.__create_video_path()
        self.predicted_sign = ''
        self.answer_color = maroon_color
        resolution = (int(self.capture.get(3)), int(self.capture.get(4)))
        self.writer = cv2.VideoWriter(self.file_name, self.video_type, self.fps, resolution)
        self.call_counter = 0
        Clock.schedule_interval(self.sign_detection_callback, 1)


    def __start_recording(self):
        self.record_video = True
        self.start_recording_time = time.time()


    def __stop_recording(self):
        self.record_video = False
        self.writer.release()


    def __model_prediction(self):
        method = get_detection_method(self.sign_type)
        prediction = method(self.file_name, self.expected_sign)
        if prediction != -1:
            return str(prediction)
        else:
            return 'Unrecognized sign'


    def initialize_instructions(self):
        # Define in subclass
        pass


    def predict_sign_from_video(self):
        self.predicted_sign = self.__model_prediction()
        self.answer_color = green_color if self.predicted_sign == self.expected_sign else red_color
        self.initialize_instructions()


    def sign_detection_callback(self, *args):
        if self.call_counter < pre_recording_time:
            self.update_instructions(f'Start recording the sign in {pre_recording_time - self.call_counter} seconds')
        
        elif self.call_counter < pre_recording_time + recording_time:
            if self.call_counter == pre_recording_time:
                self.__start_recording()
            self.update_instructions(f'Recording the sign for {pre_recording_time + recording_time - self.call_counter} seconds')

        elif self.call_counter == recording_time + pre_recording_time:
            self.__stop_recording()
            self.update_instructions('Predicting the recorded sign. Please wait ...')
            Thread(target=self.predict_sign_from_video).start()
            Clock.unschedule(self.sign_detection_callback)
        
        self.call_counter += 1

    
    def update_instructions(self, text):
        self.instructions_text = text

    
    def update_frame(self, *args):
        _, frame = self.capture.read()

        if frame is None:
            return
        
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.camera.texture = texture
        
        if self.record_video:
            self.writer.write(frame)

        if self.answer_color == green_color:
            self.end_detection()


    def end_detection(self):
        pass


    def __bind_buttons_to_stop_camera(self):
        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.bind(on_press=self.stop_camera)
        button_main.bind(on_press=self.stop_camera)


    def stop_camera(self, *args):
        self.capture.release()
        cv2.destroyAllWindows()
        button_previous = self.screen_manager.action_bar.ids.previous
        button_main = self.screen_manager.action_bar.ids.main
        button_previous.unbind(on_press=self.stop_camera)
        button_main.unbind(on_press=self.stop_camera)