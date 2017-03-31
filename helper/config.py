# -*- coding: utf-8 -*-

from os import path

# Define working directory
WORK_PATH = path.abspath(path.join(path.curdir, "stages"))

# Set True to show log messages
DEBUG = True

##########################################################################

GRAY_RATIO = [0.59, 0.30, 0.11]  # fixed
SCALE_DIM = (480, 640)           # fixed

# edge density
SOBEL_CUTOFF = 75                # keep it low

# gaussian blur
BLUR_SIZE = (60, 60)             # fixed. the kernel size
BLUR_SIGMA = (10.0, 10.0)        # proportional to blur amount
BLUR_CO = 0.004                  # proportional to blur amount

# intensity distribution
BLOCK_COUNT = (8, 8)             # decreasing = decrease quality, increase speed
WEIGHT_DIST = (0.3, 0.5)         # fixed.

# mixture model
MIXTURE_SIZE = (30, 80)          # fixed. mixture kernel size
MIXTURE_SIGMA = 3.2      		 # variance of main lobe towards x axis (keep it low)
MIXTURE_CO = (-0.2, 0.1)         # A < 0, B > 0. (A ~ 2B)
SMOOTH_CUTOFF = 200              # high value removes more noise

##########################################################################

# plate constraints
MIN_WIDTH = 70
MAX_WIDTH = 300
MIN_HEIGHT = 25
MAX_HEIGHT = 150
MIN_AREA = 1800
MAX_AREA = 30000
MIN_ASPECT = 0.20
MAX_ASPECT = 0.60

MORPH_RECT_SIZE = (10, 3)       # fixed. possible size of single character

PLATE_THRESH = 175              # high value can erase text borders
PLATE_OFFSET = 175              # high value can erase text borders

BNW_THRESH = 40                 # high value can clear entire image

CUTOFF_AVERAGE = 0.38           #


