import os
import cv2
import yaml
from types import SimpleNamespace
from number_detector import NumberDetector
from feature_extractor import HandLandmarksExtractor



if __name__ == '__main__':

    with open('train_config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config = SimpleNamespace(**config)

    image_path = 'descarga_8.png'

    feature_extractor = HandLandmarksExtractor()
    features = feature_extractor.extract_test_features(image_path)

    model = NumberDetector.create_test_model(features.shape[1], 10, config, './')
    predictions = model.predict(features)

    print(predictions)
