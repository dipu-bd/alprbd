"""
Some configuration values used everywhere
"""

import os

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
    u"ক",
    u"খ",
    u"গ",
    u"ঘ",
    u"চ",
    u"ছ",
    u"জ",
    u"ঝ",
    u"ট",
    u"ঠ",
    u"ঢ",
    u"প",
    u"ব",
    u"ভ",
    u"ম",
    u"ল",
    u"শ",
    u"স",
    u"হ"
]

# Reference https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh

# fonts - [(location, size)]
UNICODE_FONTS = [
   # ("fonts/bangla.ttf", 72),
    ("fonts/siyamrupali.ttf", 38),
    ("fonts/solaimanlipi.ttf", 46),
    ("fonts/sutonnyomj.ttf", 48)
]

# ratio between training and testing data
DATASET_RATIO = 0.85  # training data

# output directories
DIGITS_PATH = os.path.join('dataset', 'digits')
LETTERS_PATH = os.path.join('dataset', 'letters')
