"""
Some configuration values used everywhere
"""

# The numerals permitted in the vehicle registration plate : 
NUMERALS = u"০১২৩৪৫৬৭৮৯"

# The letters permitted in the vehicle registration plate 
# + Appended some letters from DistrictLetters.py
LETTERS = u"অইউএকখগঘঙচছজঝতথঢডটঠদধনপফবভমযরলশসহণষঞও"

# Reference https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh

# fonts - [(location, size)]
UNICODE_FONTS = [
    #("fonts/bangla.ttf", 72),
    ("fonts/siyamrupali.ttf", 38),
    ("fonts/solaimanlipi.ttf", 46),
    ("fonts/sutonnyomj.ttf", 48)
]

# dimension of each image
IMAGE_DIM = (28, 28)

# ratio between training and testing data
DATASET_RATIO = 0.85  # training data
