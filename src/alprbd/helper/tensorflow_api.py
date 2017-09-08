"""
For testing the trained model
"""
import os
import cv2
import numpy as np
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# The numerals permitted in the vehicle registration plate
NUMERALS = [u"০", u"১", u"২", u"৩", u"৪", u"৫", u"৬", u"৭", u"৮", u"৯"]

# The letters permitted in the vehicle registration plate
# + appended some letters from district names
LETTERS = [u"অ", u"ই", u"উ", u"এ", u"ক", u"খ", u"গ", u"ঘ", u"ঙ", u"চ", u"ছ",
           u"জ", u"ঝ", u"ত", u"থ", u"ঢ", u"ড", u"ট", u"ঠ", u"দ", u"ধ", u"ন",
           u"প", u"ফ", u"ব", u"ভ", u"ম", u"য", u"র", u"ল", u"শ", u"স", u"হ",
           u"ণ", u"ষ", u"ঞ", u"ও"]

# model files
DIGIT_PATH = os.path.join('alprbd', 'trained', 'digit.npz')
LETTER_PATH = os.path.join('alprbd', 'trained', 'letter.npz')

# input tensor
X = tf.placeholder(tf.float64, [None, 784])


class TensorFlowApi:
    """
    Provides API to convert image into text
    """

    def __init__(self):
        # Load models
        self.sess = tf.Session()
        self.digit_model = get_model(DIGIT_PATH, X)
        self.letter_model = get_model(LETTER_PATH, X)
        self.sess.run(tf.global_variables_initializer())
    # end function

    def __exit__(self, exc_type, exc_value, traceback):
        self.sess.close()
    # end function

    def recognize(self, inp, model, labels):
        """
        Recognize the given image
        :param inp:
        :param model:
        :param labels:
        :return:
        """
        inp = np.reshape(inp, [1, 784])
        out = self.sess.run(model, {X: inp}).flatten()
        return [(labels[i], round(p, 4)) for i, p in enumerate(out) if p > 1e-5]
    # end function

    def recognize_digit(self, digit):
        """
        recognize the digit
        :param digit: digit to recognize
        :return: recognition with probabilities
        """
        img = cv2.resize(digit, (28, 28))
        return self.recognize(img, self.digit_model, NUMERALS)
    # end function

    def recognize_letter(self, letter):
        """
        recognize the letter
        :param letter: letter to recognize
        :return: recognition with probabilities
        """
        img = cv2.resize(letter, (28, 28))
        return self.recognize(img, self.letter_model, LETTERS)
    # end function

    def recognize_city(self, city):
        """
        recognize the letter
        :param image: letter to recognize
        :return: recognition with probabilities
        """
        return []
    # end function

# end class


def get_model(model_file, X):
    """
    creates a tensor-flow model from given file
    :param model_file: saved model data
    :return: a tensor
    """
    model = np.load(model_file)
    w = model['weights']
    b = model['bases']
    num = w.shape[0]

    for i in range(num):
        w[i] = tf.Variable(w[i].astype(np.float64), tf.float64)
        b[i] = tf.Variable(b[i].astype(np.float64), tf.float64)

    # for each inner layers
    y = X
    for i in range(0, num - 1):
        y = tf.nn.relu(tf.matmul(y, w[i]) + b[i])

    # for the final layer
    y = tf.nn.softmax(tf.matmul(y, w[-1]) + b[-1])

    return y
# end functions