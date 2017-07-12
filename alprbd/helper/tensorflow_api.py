"""
For testing the trained model
"""
import os
import cv2
import numpy as np
import tensorflow as tf

# The numerals permitted in the vehicle registration plate
NUMERALS = [u"০", u"১", u"২", u"৩", u"৪", u"৫", u"৬", u"৭", u"৮", u"৯"]

# The letters permitted in the vehicle registration plate
# + appended some letters from district names
LETTERS = [u"অ", u"ই", u"উ", u"এ", u"ক", u"খ", u"গ", u"ঘ", u"ঙ", u"চ", u"ছ",
           u"জ", u"ঝ", u"ত", u"থ", u"ঢ", u"ড", u"ট", u"ঠ", u"দ", u"ধ", u"ন",
           u"প", u"ফ", u"ব", u"ভ", u"ম", u"য", u"র", u"ল", u"শ", u"স", u"হ",
           u"ণ", u"ষ", u"ঞ", u"ও"]

# Create session
sess = tf.Session()

# Restore model
model_folder = os.path.join('alprbd', 'trained', 'digit')
model_folder = os.path.abspath(model_folder)
model_file = os.path.join(model_folder, 'model.meta')
print(model_file)
saver = tf.train.import_meta_graph(model_file)
saver.restore(sess, tf.train.latest_checkpoint(model_folder))

graph = tf.get_default_graph()
X = graph.get_tensor_by_name("X:0")
Y = graph.get_tensor_by_name("Y:0")
pkeep = graph.get_tensor_by_name("pkeep:0")

def recognize(img, model_folder, labels):
    """
    Recognize the given image
    :param img:
    :param model_folder:
    :param labels:
    :return:
    """
    # prepare image data
    img = np.reshape(img, (1, 784))

    # predict outcome
    out = sess.run(Y, {X: img, pkeep: 1.0}).flatten()
    result = [(labels[i], round(p, 4)) for i, p in enumerate(out) if p > 1e-4]
    return result
# end function


def recognize_digit(digit):
    """
    recognize the digit
    :param digit: digit to recognize
    :return: recognition with probabilities
    """
    img = cv2.resize(digit, (28, 28))
    folder = os.path.join('alprbd', 'trained', 'digit')
    return recognize(img, folder, NUMERALS)
# end function


def recognize_letter(letter):
    """
    recognize the letter
    :param letter: letter to recognize
    :return: recognition with probabilities
    """
    img = cv2.resize(letter, (28, 28))
    folder = os.path.join('alprbd', 'trained', 'letter')
    return [] #recognize(img, folder, LETTERS)
# end function


def recognize_city(image):
    """
    recognize the letter
    :param image: letter to recognize
    :return: recognition with probabilities
    """
    return []
# end function

