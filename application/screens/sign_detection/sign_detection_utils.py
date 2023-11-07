from detectors.detect_sign import detect_letter_sign, detect_number_sign, detect_word_sign
from constants import number_type, word_type, letter_type



def get_detection_method(sign_type):
    if sign_type == number_type:
        return detect_number_sign
    elif sign_type == letter_type:
        return detect_letter_sign
    elif sign_type == word_type:
        return detect_word_sign
    else:
        raise ValueError(sign_type)