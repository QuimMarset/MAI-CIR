import os
import numpy as np
from PIL import Image
from skimage import img_as_ubyte



if __name__ == '__main__':

    images_npy_path = os.path.join('datasets', 'numbers_0_9', 'X.npy')
    labels_path = os.path.join('datasets', 'numbers_0_9', 'Y.npy')

    with open(images_npy_path, 'rb') as file:
        images = np.load(file)

    with open(labels_path, 'rb') as file:
        labels = np.load(file)

    images_path = os.path.join('datasets', 'numbers_0_9', 'images')
    os.makedirs(images_path, exist_ok=True)

    unique_labels = np.unique(labels)
    interesting_labels = unique_labels[:10]

    for label in interesting_labels:
        os.makedirs(os.path.join(images_path, label), exist_ok=True)

    for image, label in zip(images, labels):
        label = label[0]
        if label not in interesting_labels:
            continue

        image_pil = Image.fromarray(img_as_ubyte(image))
        folder_path = os.path.join(images_path, label)
        image_pil.save(os.path.join(folder_path, f'image_{len(os.listdir(folder_path))}.png'))

