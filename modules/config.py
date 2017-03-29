# -*- coding: utf-8 -*-

from os import path

# Define working directory
WORK_PATH = path.abspath(path.join(path.curdir, "stages"))

# Set True to show log messages
DEBUG = True

# Values defined in paper
GRAY_RATIO = [0.59, 0.30, 0.11]  # fixed
SCALE_DIM = (480, 640)          # fixed

SOBEL_CUTOFF = 127              # should keep it low

BLUR_SIZE = (60, 60)            # the kernel size
BLUR_SIGMA = (5.0, 5.0)         # proportional to blur amount
BLUR_COE = 0.004                # proportional to blur amount

BLOCK_COUNT = (8, 8)            # decreasing will decrease quality but increase speed
WEIGHT_DIST = (0.3, 0.5)        #

MIXTURE_SIZE = (30, 80)         # mixture kernal size
MIXTURE_SIGMA = (2.0, 1.0)      # higher value will dilate regions
MIXTURE_COEFF = (-1.2, 0.6)     # higher value will dilate regions

SMOOTH_CUTOFF = 128             # can be high for removing noise
BNW_THRESH = 75                 # high value can clear entire image


MIN_PLATE_SIZE = (25, 60)       #
MAX_PLATE_SIZE = (300, 400)     #

MORPH_RECT_SIZE = (10, 3)       #
CUTOFF_AVERAGE = 0.38           #
