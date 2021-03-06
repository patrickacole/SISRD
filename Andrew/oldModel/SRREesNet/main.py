import os
import numpy as np
import cv2
import neural_net
import argparse


def load_images(path):
    data = []
    for file in sorted(os.listdir(path)):
        img = cv2.imread(path + file, 0)
        w, h = img.shape
        if w == 64 and h == 64:
            img = cv2.resize(img, (128,128), interpolation=cv2.INTER_CUBIC)
        w, h = img.shape
        img = img.reshape((w,h,1))
        img = img.astype(np.float32) / 255
        data.append(img)
    return np.array(data)

def save_images(path, imageNames, images):
    names = sorted(os.listdir(imageNames))
    for file, i in zip(names, np.arange(len(names))):
        img = images[i]
        w, h, _ = img.shape
        img = img.reshape((w,h))
        img = img * 255
        img = img.astype(np.uint8)
        cv2.imwrite(path + file, img)
    return

def main():
    test_64_path = "xray/test_images_64x64/"
    test_128_path = "xray/test_images_128x128/"
    train_64_path = "xray/train_images_64x64/"
    train_128_path = "xray/train_images_128x128/"

    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--model")
    args = parser.parse_args()

    if args.model:
        if args.train:
            print("Creating model...")
            nn = neural_net.createModel()
            print("Loading images...")
            train_input = load_images(train_64_path)
            print(train_input.shape)
            train_output = load_images(train_128_path)
            print(train_output.shape)
            print("Training model...")
            nn.fit(train_input, train_output, batch_size=128, epochs=20)
            print("Saving model")
            nn.save(args.model)
            if args.test:
                print("Loading test images...")
                test_images_64 = load_images(test_64_path)
                print("Predicting...")
                test_out_128 = nn.predict(test_images_64)
                print(test_out_128.shape)
                if not os.path.exists(test_128_path):
                    os.makedirs(test_128_path)
                print("Saving images...")
                save_images(test_128_path, test_64_path, test_out_128)
        elif args.test:
            print("Loading model...")
            nn = neural_net.loadModel(args.model)
            print("Loading test images...")
            test_images_64 = load_images(test_64_path)
            print("Predicting...")
            test_out_128 = nn.predict(test_images_64)
            print(test_out_128.shape)
            print("Saving images...")
            save_images(test_128_path, test_64_path, test_out_128)
        else:
            print("Usage: main.py <--train/--test> --model <model_name>")
            exit(1)
    else:
        print("Usage: main.py <--train/--test> --model <model_name>")
        exit(1)

main()
