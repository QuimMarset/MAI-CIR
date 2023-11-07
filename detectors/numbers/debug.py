import numpy as np
import cv2
import os
import time
import yaml
from types import SimpleNamespace
import mediapipe as mp
mp_hands = mp.solutions.hands
from number_detector import NumberDetector
from feature_extractor import HandLandmarksExtractor



def detect_number_sign(video_path, config):
    landmark_extractor = HandLandmarksExtractor()
    features = landmark_extractor.extract_video_features(video_path)
    if len(features) > 0:
        model = NumberDetector.create_test_model(features.shape[1], 10, config, './')
        predictions = model.predict(features)
        print(predictions)
        values, counts = np.unique(predictions, return_counts=True)
        return values[np.argmax(counts)]
    return 0


def record_video():
    cap = cv2.VideoCapture('http://192.168.1.132:8080/video')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    writer = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

    start_time = time.time()
    print('START!')
    while True:
        ret, frame= cap.read()
        writer.write(frame)

        if time.time() - start_time > 4:
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':

    with open('train_config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config = SimpleNamespace(**config)

    record_video()

    video_path = 'video.mp4'

    sign = detect_number_sign(video_path, config)
    print(sign)