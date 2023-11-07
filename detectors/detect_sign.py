import numpy as np
import yaml
from types import SimpleNamespace
from detectors.words.word_detector import detect_sign
from detectors.numbers import number_detector, feature_extractor
from detectors.alphabet.alphabet_detector import AlphabetDetector
from constants import numbers_model_config_path, numbers_model_path


# ==========
# Numbers
# ==========

def load_config():
    with open(numbers_model_config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config = SimpleNamespace(**config)
    return config


def detect_number_sign(video_path, expected_sign):
    train_config = load_config()
    landmark_extractor = feature_extractor.HandLandmarksExtractor()
    features = landmark_extractor.extract_video_features(video_path)
    if len(features) > 0:
        model = number_detector.NumberDetector.create_test_model(features.shape[1], 10, train_config, numbers_model_path)
        predictions = model.predict(features)
        values, counts = np.unique(predictions, return_counts=True)
        return values[np.argmax(counts)]
    return -1


# ==========
# Letters
# ==========


def check_if_expected_in_predictions(predictions, expected_sign):
    for prediction in predictions:
        if prediction == expected_sign:
            return expected_sign
    values, counts = np.unique(predictions, return_counts=True)
    return values[np.argmax(counts)]


def detect_letter_sign(video_path, expected_sign):
    detector = AlphabetDetector()
    predictions = detector.predict_alphabet_sign(video_path)
    flattened = np.reshape(predictions, -1)
    if len(flattened) == 0:
        return -1
    elif len(flattened) == 1:
        return flattened[0]
    else:
        return check_if_expected_in_predictions(flattened, expected_sign)


# ==========
# Words
# ==========

def detect_word_sign(video_path, expected_sign):
    predictions = detect_sign(video_path)
    for prediction in predictions[:5]:
        if prediction[0] == expected_sign:
            return expected_sign
    return predictions[0][0]
    