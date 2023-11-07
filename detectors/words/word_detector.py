import copy
import torch
import numpy as np
import sys
sys.path.insert(0, './detectors/words')
from spoter_mod.skeleton_extractor import obtain_pose_data
from spoter_mod.normalization.body_normalization import normalize_single_dict as normalize_single_body_dict, BODY_IDENTIFIERS
from spoter_mod.normalization.hand_normalization import normalize_single_dict as normalize_single_hand_dict, HAND_IDENTIFIERS
from constants import words_model_path


device = torch.device('cpu')
if torch.cuda.is_available():
    device = torch.device('cuda')


HAND_IDENTIFIERS = [id + "_Left" for id in HAND_IDENTIFIERS] + [id + "_Right" for id in HAND_IDENTIFIERS]
GLOSS = ['book', 'drink', 'computer', 'before', 'chair', 'go', 'clothes', 'who', 'candy', 'cousin', 'deaf', 'fine',
         'help', 'no', 'thin', 'walk', 'year', 'yes', 'all', 'black', 'cool', 'finish', 'hot', 'like', 'many', 'mother',
         'now', 'orange', 'table', 'thanksgiving', 'what', 'woman', 'bed', 'blue', 'bowling', 'can', 'dog', 'family',
         'fish', 'graduate', 'hat', 'hearing', 'kiss', 'language', 'later', 'man', 'shirt', 'study', 'tall', 'white',
         'wrong', 'accident', 'apple', 'bird', 'change', 'color', 'corn', '""cow""', 'dance', 'dark', 'doctor', 'eat',
         'enjoy', 'forget', 'give', 'last', 'meet', 'pink', 'pizza', 'play', 'school', 'secretary', 'short', 'time',
         'want', 'work', 'africa', 'basketball', 'birthday', 'brown', 'but', 'cheat', 'city', 'cook', 'decide', 'full',
         'how', 'jacket', 'letter', 'medicine', 'need', 'paint', 'paper', 'pull', 'purple', 'right', 'same', 'son',
         'tell', 'thursday']


def load_model():
    model = torch.load(words_model_path, map_location=device)
    model.train(False)
    return model


def tensor_to_dictionary(landmarks_tensor: torch.Tensor) -> dict:
    data_array = landmarks_tensor.numpy()
    output = {}

    for landmark_index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        output[identifier] = data_array[:, landmark_index]

    return output


def dictionary_to_tensor(landmarks_dict: dict) -> torch.Tensor:
    output = np.empty(shape=(len(landmarks_dict["leftEar"]), len(BODY_IDENTIFIERS + HAND_IDENTIFIERS), 2))

    for landmark_index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        output[:, landmark_index, 0] = [frame[0] for frame in landmarks_dict[identifier]]
        output[:, landmark_index, 1] = [frame[1] for frame in landmarks_dict[identifier]]

    return torch.from_numpy(output)


def detect_sign(video_path):
    model = load_model()
    data = obtain_pose_data(video_path)
    depth_map = np.empty(shape=(len(data.data_hub["nose_X"]), len(BODY_IDENTIFIERS + HAND_IDENTIFIERS), 2))

    for index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        depth_map[:, index, 0] = data.data_hub[identifier + "_X"]
        depth_map[:, index, 1] = data.data_hub[identifier + "_Y"]

    depth_map = torch.from_numpy(np.copy(depth_map))
    depth_map = tensor_to_dictionary(depth_map)

    keys = copy.copy(list(depth_map.keys()))
    for key in keys:
        data = depth_map[key]
        del depth_map[key]
        depth_map[key.replace("_Left", "_0").replace("_Right", "_1")] = data

    depth_map = normalize_single_body_dict(depth_map)
    depth_map = normalize_single_hand_dict(depth_map)

    keys = copy.copy(list(depth_map.keys()))
    for key in keys:
        data = depth_map[key]
        del depth_map[key]
        depth_map[key.replace("_0", "_Left").replace("_1", "_Right")] = data

    depth_map = dictionary_to_tensor(depth_map)
    depth_map = depth_map - 0.5

    inputs = depth_map.squeeze(0).to(device)
    outputs = model(inputs).expand(1, -1, -1)
    results = torch.nn.functional.softmax(outputs, dim=2).detach().numpy()[0, 0]

    results = {GLOSS[i]: float(results[i]) for i in range(100)}
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    return sorted_results