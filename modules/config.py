# -*- coding: utf-8 -*-

from os import path

# Define working directory
WORK_PATH = path.join(path.curdir, "stages")

DEBUG = True    # True to show messages

GRAY_RATIO = [0.59, 0.30, 0.11]
SCALE_DIM = (480, 640)

BNW_THRESH = 75
SOBEL_CUTOFF = 0.042
SMOOTH_CUTOFF = 0.36

BLUR_SIZE = (60, 60)
BLUR_SIGMA = (10.0, 10.0)
BLUR_COEFF = 0.004

WEIGHT_DIST = (0.3, 0.5)
BLOCK_COUNT = (8, 8)

MIXTURE_SIZE = (30, 80)
MIXTURE_SIGMA = (2.0, 1.0)
MIXTURE_COEFF = (-2.4, 1.2)

MIN_PLATE_SIZE = (25, 60)
MAX_PLATE_SIZE = (300, 400)

MORPH_RECT_SIZE = (10, 3)
CUTOFF_AVERAGE = 0.38
