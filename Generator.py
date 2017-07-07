"""
Generates basic dataset
"""
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import config as cfg

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Necessary variables
INDEX = 0
FRAME = np.zeros([100, 300], dtype=np.uint8)

# Create output path
OUTPUT_PATH = os.path.join('output', 'generated')


def check_path(output):
    """
    if a directory does not exists, creates it.
    """
    if not os.path.exists(output):
        os.makedirs(output)
    #end if
# end function


def trim_image(img_file):
    """
    Trims the image
    """
    # open
    img = cv2.imread(img_file, 0)
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 2)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 2)
    # crop
    cropped = img[x1:x2, y1:y2]
    # resize
    resized = cv2.resize(cropped, cfg.IMAGE_DIM)
    # save
    cv2.imwrite(img_file, resized)
# end function


def generate(data, font):
    """
    Generates images for every letters given in the array
    """
    global INDEX

    for letter, label in data.items():
        INDEX += 1
        # create a grayscale image
        img = Image.fromarray(FRAME)
        # get graphics
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), letter, 255, font=font)
        # save image
        name = '{:03d}.bmp'.format(INDEX)
        save_to = os.path.join(OUTPUT_PATH, label)
        check_path(save_to)
        save_to = os.path.join(save_to, name)
        img.save(save_to)
        # trim image
        trim_image(save_to)
    # end for
# end function


def run():
    """
    To generate the image from the texts
    """
    for font_path, font_size in cfg.UNICODE_FONTS:
        font = ImageFont.truetype(font_path, font_size)
        generate(cfg.LETTER_LABELS, font)
        generate(cfg.NUMERAL_LABELS, font)
    # end for
# end if
