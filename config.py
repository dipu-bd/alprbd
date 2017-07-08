"""
Some configuration values used everywhere
"""

import os

# dimension of each image
IMAGE_DIM = (28, 28)

# dataset directories
DIGITS_PATH = os.path.join('dataset', 'digits')
LETTERS_PATH = os.path.join('dataset', 'letters')

# model directories
DIGIT_MODEL = os.path.join('OCRModels', 'digit', 'model')
LETTER_MODEL = os.path.join('OCRModels', 'letter', 'model')

# sample directory
DIGIT_SAMPLES = 'sample/digits'
LETTER_SAMPLES = 'sample/letters'

# log directory
DIGIT_LOGS = 'logs/digits'
LETTER_LOGS = 'logs/letters'

# The numerals permitted in the vehicle registration plate
NUMERALS = [
    u"০",
    u"১",
    u"২",
    u"৩",
    u"৪",
    u"৫",
    u"৬",
    u"৭",
    u"৮",
    u"৯",
]

# The letters permitted in the vehicle registration plate
# + appended some letters from district names
LETTERS = [
    u"অ",
    u"ই",
    u"উ",
    u"এ",
    u"ক",
    u"খ",
    u"গ",
    u"ঘ",
    u"ঙ",
    u"চ",
    u"ছ",
    u"জ",
    u"ঝ",
    u"ত",
    u"থ",
    u"ঢ",
    u"ড",
    u"ট",
    u"ঠ",
    u"দ",
    u"ধ",
    u"ন",
    u"প",
    u"ফ",
    u"ব",
    u"ভ",
    u"ম",
    u"য",
    u"র",
    u"ল",
    u"শ",
    u"স",
    u"হ",

    u"ণ",
    u"ষ",
    u"ঞ",
    u"ও",
]

# Reference https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh
