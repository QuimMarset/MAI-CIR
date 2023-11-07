import yaml
from types import SimpleNamespace
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from custom_dataset import CustomDataset
from feature_extractor import HandLandmarksExtractor
from number_detector import NumberDetector




def create_dataframe(images_paths, labels):
    return pd.DataFrame({'image_path' : images_paths, 'label' : labels})


def create_dataset(dataset_path):
    images_paths = []
    labels = []

    for subfolder in os.listdir(dataset_path):
        label = int(subfolder)
        subfolder_path = os.path.join(dataset_path, subfolder)

        for image_name in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image_name)
            images_paths.append(image_path)
            labels.append(label)

    return images_paths, labels


def create_train_dataset(*train_paths):
    images_paths = []
    labels = []

    for train_path in train_paths:
        images_paths_i, labels_i = create_dataset(train_path)
        images_paths.extend(images_paths_i)
        labels.extend(labels_i)

    return images_paths, labels
    

def create_train_val_split(images_paths, labels, val_size=0.1):
    return train_test_split(images_paths, labels, test_size=val_size, stratify=labels)


def create_test_dataset(test_path):
    return create_dataset(test_path)


def create_data_loader(features, labels, num_classes, batch_size, shuffle=True):
    dataset = CustomDataset(features, labels, num_classes)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return data_loader



if __name__ == '__main__':

    with open('train_config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config = SimpleNamespace(**config)

    train_1_path = os.path.join('datasets', 'train', 'numbers_1_9')
    train_2_path = os.path.join('datasets', 'train', 'numbers_0_9')
    train_3_path = os.path.join('datasets', 'train', 'numbers_0_9_2')
    test_path = os.path.join('datasets', 'test')
    
    train_image_paths, train_labels = create_train_dataset(train_1_path, train_2_path, train_3_path)
    train_image_paths, val_image_paths, train_labels, val_labels = create_train_val_split(train_image_paths, train_labels)
    test_image_paths, test_labels = create_test_dataset(test_path)

    feature_extractor = HandLandmarksExtractor()

    print(len(train_image_paths), len(val_image_paths), len(test_image_paths))

    train_features, train_labels = feature_extractor.extract_train_features(train_image_paths, train_labels)
    val_features, val_labels = feature_extractor.extract_train_features(val_image_paths, val_labels)
    test_features, test_labels = feature_extractor.extract_train_features(test_image_paths, test_labels)

    print(train_features.shape[0], val_features.shape[0], test_features.shape[0])

    num_classes = len(os.listdir(test_path))

    model = NumberDetector(train_features.shape[1], config, num_classes)
    model.train_model(train_features, train_labels, val_features, val_labels, './')
    model.evaluate_model(test_features, test_labels, './')