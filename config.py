"""
Some configuration values used everywhere
"""

import os

# dimension of each image
IMAGE_DIM = (28, 28)
CITY_DIM = (28, 4*28)

# dataset directories
DIGITS_PATH = os.path.join('dataset', 'digits')
LETTERS_PATH = os.path.join('dataset', 'letters')
CITY_PATH = os.path.join('dataset', 'city')

# model directories
DIGIT_MODEL = os.path.join('trained', 'digit.npz')
LETTER_MODEL = os.path.join('trained', 'letter.npz')
CITY_MODEL = os.path.join('trained', 'city.npz')

# sample directory
DIGIT_SAMPLES = 'sample/digits'
LETTER_SAMPLES = 'sample/letters'

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

    #u"ণ",
    u"ষ",
    u"ঞ",
    u"ও",
]

CITIES = [
    u"বরগুনা",
    u"বরিশাল",
    u"ভোলা",
    u"ঝালকাঠি",
    u"পটুয়াখালী",
    u"পিরোজপুর",
    u"বান্দরবান",
    u"ব্রাহ্মণবাড়ীয়া",
    u"চাঁদপুর",
    u"চট্ট",
    u"কুমিল্লা",
    u"কক্সবাজার",
    u"ফেনী",
    u"খাগড়াছড়ি",
    u"লক্ষ্মীপুর",
    u"নোয়াখালী",
    u"রাঙ্গামাটি",
    u"ঢাকা",
    u"ফরিদপুর",
    u"গাজীপুর",
    u"গোপালগঞ্জ",
    u"কিশোরগঞ্জ",
    u"মাদারীপুর",
    u"মানিকগঞ্জ",
    u"মুন্সীগঞ্জ",
    u"নারায়ণগঞ্জ",
    u"নরসিংদী",
    u"রাজবাড়ী",
    u"শরীয়তপুর",
    u"টাঙ্গাইল",
    u"বাগেরহাট",
    u"চুয়াডাঙ্গা",
    u"যশোর",
    u"ঝিনাইদহ",
    u"খুলনা",
    u"কুষ্টিয়া",
    u"মাগুরা",
    u"মেহেরপুর",
    u"নড়াইল",
    u"সাতক্ষিরা",
    u"জামালপুর",
    u"ময়মনসিংহ",
    u"নেত্রকোনা",
    u"শেরপুর",
    u"বগুড়া",
    u"জয়পুরহাট",
    u"নওগাঁ",
    u"নাটোর",
    u"নওয়াবগঞ্জ",
    u"পাবনা",
    u"রাজশাহী",
    u"সিরাজগঞ্জ",
    u"দিনাজপুর",
    u"গাইবান্ধা",
    u"কুড়িগ্রাম",
    u"লালমনিরহাট",
    u"নীলফামারী",
    u"পঞ্চগড়",
    u"রংপুর",
    u"ঠাকুরগাঁও",
    u"হবিগঞ্জ",
    u"মৌলভীবাজার",
    u"সুনামগঞ্জ",
    u"সিলেট",
]

# Reference https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Bangladesh
