"""
Some utility functions
"""

import os
import collections
import numpy as np
import config as cfg
from Dataset import Dataset

VALIDATION_RATIO = 0.1
DIGIT_PATH = os.path.join('dataset', 'digits')
LETTER_PATH = os.path.join('dataset', 'letters')

def dense_to_one_hot(labels, letters):
    """Returns one-hot representation of the labels"""
    labels = [letters.index(x) for x in labels]
    num_labels = len(labels)
    num_classes = len(letters)
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

    # build validation set
    num_validation = len(train_images) * VALIDATION_RATIO
    validation_images = train_images[:num_validation]    
    validation_labels = train_labels[:num_validation]    
    train_images = train_images[num_validation:]
    train_labels = train_labels[num_validation:]

    # get testing set
    test_images = os.path.join(folder, 'testing_data.npy')
    test_labels = os.path.join(folder, 'testing_labels.npy')
    test_images = np.load(test_images)
    test_labels = np.load(test_labels)

    # convert to one-hot
    train_labels = dense_to_one_hot(train_labels, letters)
    validation_labels = dense_to_one_hot(validation_labels, letters)
    test_labels = dense_to_one_hot(test_labels, letters)

    train = Dataset(train_images, train_labels)
    validation = Dataset(validation_images, validation_labels)
    test = Dataset(test_images, test_labels)

    ds = collections.namedtuple('Datasets', ['train', 'validation', 'test'])
    return ds(train=train, validation=validation, test=test)
# end function

def get_digit_data():
    return get_data(cfg.DIGITS_PATH, cfg.DIGITS)
# end function

def get_letter_data():
    return get_data(LETTERS_PATH, cfg.LETTERS)
# end function
