# -*- coding: utf-8 -*-

from os import path

# Define working directory
WORK_PATH = path.abspath(path.join(path.curdir, "stages"))

# Set True to show log messages
DEBUG = True

GRAY_RATIO = [0.59, 0.30, 0.11]  # fixed
SCALE_DIM = (480, 640)           # fixed

SOBEL_CUTOFF = 127              # keep it low

BLUR_SIZE = (60, 60)            # fixed. the kernel size
BLUR_SIGMA = (10.0, 10.0)       # proportional to blur amount
BLUR_CO = 0.004                 # proportional to blur amount

BLOCK_COUNT = (8, 8)            # fixed. decreasing will decrease quality but increase speed
WEIGHT_DIST = (0.3, 0.5)        # fixed.

MIXTURE_SIZE = (30, 80)         # fixed. mixture kernel size
MIXTURE_SIGMA = (2.0, 1.0)      # control height,width of matched area
MIXTURE_CO = (-1.2, 0.6)        # difference between black and white dora

SMOOTH_CUTOFF = 225             # set high value for removing noise

MIN_PLATE_SIZE = (25, 60)       # minimum height, minimum width
MAX_PLATE_SIZE = (300, 400)     # maximum height, maximum width
PLATE_AREA = (1500, 100000)     # minimum area, maximum area

MORPH_RECT_SIZE = (10, 3)       # fixed. possible size of single character

PLATE_THRESH = 175              # high value can erase text borders
PLATE_OFFSET = 175              # high value can erase text borders

BNW_THRESH = 40                 # high value can clear entire image

CUTOFF_AVERAGE = 0.38           #


