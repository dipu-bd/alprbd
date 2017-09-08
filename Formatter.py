"""
Formats images to feed into tensorflow
"""
# -*- coding: utf-8 -*-

import os
from glob import glob
import cv2
import numpy as np
import config as cfg

def read_images(folder):
    return [file for file in glob(folder + '/**/*.bmp', recursive=True)]
# end if

def get_train_files(folder):
    data_file = os.path.join(folder, 'training_data.npy')
    label_file = os.path.join(folder, 'training_labels.npy')
    return data_file, label_file
# end function

def get_test_files(folder):
    data_file = os.path.join(folder, 'testing_data.npy')
    label_file = os.path.join(folder, 'testing_labels.npy')
    return data_file, label_file
# end function

def save_separated(images, files):
    data = []
    labels = []
    for img in images:
        # add label
        label = img.split(os.sep)[-2]
        labels.append(label)
        # read and flatten image
        image = cv2.imread(img, 0)
        data.append(image.flatten())
    # end for

    # save to file
    (data_file, label_file) = files
    np.save(data_file, np.array(data))
    np.save(label_file, np.array(labels))
# end function


def test_integrity(folder):    
    _, train_labels = get_train_files(folder)
    _, test_labels = get_test_files(folder)
    # training labels
    labels = np.load(train_labels);
    train = dict()
    for x in labels:
        if x in train:
            train[x] += 1
        else:
            train[x] = 1
    # end for
    print("Training labels:", len(train.keys()))

    # testing labels
    labels = np.load(test_labels);
    test = dict()
    for x in labels:
        if x in test:
            test[x] += 1
        else:
            test[x] = 1
    # end for
    print("Testing labels:", len(test.keys()))

    # check
    if len(train.keys()) == len(test.keys()):
        print("Integrity check: **OK**.")
    else: 
        print("Integrity check !!FAILED!!.")
    # end if
# end function


def format_docs(folder):
    print('\nFormatting', folder, '...')
    # get all image files
    images = np.array(read_images(folder))
    # suffle them
    np.random.shuffle(images)
    # separate training and testing
    pos = int(len(images) * cfg.DATASET_RATIO)
    training = images[:pos]
    testing = images[pos:]
    # a little printout
    print("Total images:", len(images))
    print("Training:", len(training))
    print("Testing:", len(testing))
    # separate labels and image data
    save_separated(training, get_train_files(folder))
    save_separated(testing, get_test_files(folder))
    print("Formatting done.")
    test_integrity(folder);
# end if

if __name__ == '__main__':
    format_docs(cfg.DIGITS_PATH)
    format_docs(cfg.LETTERS_PATH)
# end if
