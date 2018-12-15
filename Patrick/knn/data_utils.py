import numpy as np
from cv2 import imread, imwrite, resize, INTER_CUBIC
from os import listdir

def load_data(path):
    data = []
    for file in sorted(listdir(path)):
        img = imread(path + file, 0)
        img = img.astype(np.float32)
        data.append(img)
    return np.array(data)

def save_images(path, imageNames, images):
    names = sorted(listdir(imageNames))
    for file, i in zip(names, np.arange(len(names))):
        img = images[i]
        img = img.astype(np.uint8)
        imwrite(path + file, img)
    return

if __name__ == "__main__":
    print("data_utils test")
    imgs = load_data('xray_images/train_images_64x64/')
    save_images('test/', 'xray_images/train_images_64x64/', imgs)
