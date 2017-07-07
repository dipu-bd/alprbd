# The letters permitted in the vehicle registration plate
# Source: https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh
LETTERS = u"অইউএকখগঘঙচছজঝতথঢডটঠদধনপফবভমযরলশসহ"

LETTER_LABELS = {
    u"অ": "O",
    u"ই": "E",
    u"উ": "U",
    u"এ": "A",
    u"ক": "K",
    u"খ": "Kha",
    u"গ": "G",
    u"ঘ": "Gha",
    u"ঙ": "Uo",
    u"চ": "C",
    u"ছ": "Cha",
    u"জ": "J",
    u"ঝ": "Jha",
    u"ত": "Ta",
    u"থ": "Tha",
    u"ঢ": "Dhw",
    u"ড": "Dw",
    u"ট": "To",
    u"ঠ": "Tho",
    u"দ": "Da",
    u"ধ": "Dha",
    u"ন": "N",
    u"প": "P",
    u"ফ": "F",
    u"ব": "B",
    u"ভ": "V",
    u"ম": "M",
    u"য": "Z",
    u"র": "R",
    u"ল": "L",
    u"শ": "Sh",
    u"স": "S",
    u"হ": "H"
}

# The numerals permitted in the vehicle registration plate
# Source: https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh
NUMERALS = u"০১২৩৪৫৬৭৮৯"

NUMERAL_LABELS = {
    u"০": "0",
    u"১": "1",
    u"২": "2",
    u"৩": "3",
    u"৪": "4",
    u"৫": "5",
    u"৬": "6",
    u"৭": "7",
    u"৮": "8",
    u"৯": "9"
}

# fonts - [(location, size)]
UNICODE_FONTS = [
    #("fonts/bangla.ttf", 72),
    ("fonts/siyamrupali.ttf", 38),
    ("fonts/solaimanlipi.ttf", 46),
    ("fonts/sutonnyomj.ttf", 48)
]

BIJOY_FONTS = [
    ("fonts/sutonnymj.ttf", 48),
]

# dimension of each image
IMAGE_DIM = (28, 28)

# ratio between training and testing data
DATASET_RATIO = 0.85  # training data
