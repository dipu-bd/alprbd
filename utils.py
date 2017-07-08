"""
Some utility functions
"""

import os
import numpy as np

DIGIT_PATH = os.path.join('dataset', 'digits')
LETTER_PATH = os.path.join('dataset', 'letters')

def get_data(folder):
    train_data = os.path.join(folder, 'training_data.npy')
    train_labels = os.path.join(folder, 'training_labels.npy')
    train_data = np.load(train_data)
    train_labels = np.load(train_labels)

    test_data = os.path.join(folder, 'testing_data.npy')
    test_labels = os.path.join(folder, 'testing_labels.npy')
    test_data = np.load(test_data)
    test_labels = np.load(test_labels)

    return ((train_data, train_labels), (test_data, test_labels))
# end function

def get_digit_data():
    return get_data(DIGIT_PATH)
# end function

def get_letter_data():
    return get_data(LETTER_PATH)
# end function
