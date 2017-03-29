# -*- coding: utf-8 -*-

from os import path

# Define working directory
WORK_PATH = path.abspath(path.join(path.curdir, "stages"))

# Set True to show log messages
DEBUG = True

# Values defined in paper
GRAY_RATIO = [0.59, 0.30, 0.11]  # fixed
SCALE_DIM = (480, 640)          # fixed

SOBEL_CUTOFF = 0.042            # should keep it low
SMOOTH_CUTOFF = 0.36            # can be high for removing noise
BNW_THRESH = 75                 # high value can clear entire image

BLUR_SIZE = (60, 60)            #
BLUR_SIGMA = (10.0, 10.0)       #
BLUR_COEFF = 0.004              #

WEIGHT_DIST = (0.3, 0.5)        #
BLOCK_COUNT = (8, 8)            #

MIXTURE_SIZE = (30, 80)         #
MIXTURE_SIGMA = (2.0, 1.0)      #
MIXTURE_COEFF = (-2.4, 1.2)     #

MIN_PLATE_SIZE = (25, 60)       #
MAX_PLATE_SIZE = (300, 400)     #

MORPH_RECT_SIZE = (10, 3)       #
CUTOFF_AVERAGE = 0.38           #
