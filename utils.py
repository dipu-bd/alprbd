# -*- coding: utf-8 -*-
"""
Some utility functions
"""

import os
import collections
import numpy as np
import config as cfg
from Dataset import Dataset

def dense_to_one_hot(labels, classes):
    """Returns one-hot representation of the labels"""
    labels = [classes.index(x) for x in labels]
    num_labels = len(labels)
    num_classes = len(classes)
    index_offset = np.arange(num_labels) * num_classes
    labels_one_hot = np.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + np.ravel(labels)] = 1
    return labels_one_hot
# end function

def get_data(folder, letters):
    """Build the dataset"""
    # get training set
    train_images = os.path.join(folder, 'training_data.npy')
    train_labels = os.path.join(folder, 'training_labels.npy')
    train_images = np.load(train_images)
    train_labels = np.load(train_labels)

    # get testing set
    test_images = os.path.join(folder, 'testing_data.npy')
    test_labels = os.path.join(folder, 'testing_labels.npy')
    test_images = np.load(test_images)
    test_labels = np.load(test_labels)

    # convert to one-hot
    train_labels = dense_to_one_hot(train_labels, letters)
    test_labels = dense_to_one_hot(test_labels, letters)

    # build Dataset objects
    train = Dataset(train_images, train_labels)
    test = Dataset(test_images, test_labels)
    ds = collections.namedtuple('Datasets', ['train', 'test'])
    return ds(train=train, test=test)
# end function

def get_digit_data():
    return get_data(cfg.DIGITS_PATH, cfg.NUMERALS)
# end function

def get_letter_data():
    return get_data(cfg.LETTERS_PATH, cfg.LETTERS)
# end function