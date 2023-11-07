from torch.utils.data.dataset import Dataset
import numpy as np


class CustomDataset:

    def __init__(self, features, labels, num_labels):
        self.features = features
        num_samples = len(labels)
        self.labels = np.zeros((num_samples, num_labels))
        self.labels[range(num_samples), labels] = 1


    def __getitem__(self, index):
        return self.features[index], self.labels[index]


    def __len__(self):
        return self.features.shape[0]