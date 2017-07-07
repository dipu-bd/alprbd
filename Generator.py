# -*- coding: utf-8 -*-

import os
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


def checkPath(output):
    if not os.path.exists(output):
        os.makedirs(output)
    #end if
# end function


def trim(img):
    """
    Trims the image
    """
    img_arr = np.array(img)
    rows, cols = img_arr.shape
    nzx, nzy = np.nonzero(img_arr)
    x1 = max(0, np.min(nzx) - 3)
    x2 = min(rows, np.max(nzx) + 3)
    y1 = max(0, np.min(nzy) - 3)
    y2 = min(cols, np.max(nzy) + 3)
    cropped = img_arr[x1:x2, y1:y2]
    return Image.fromarray(cropped)
# end function


def generate(data, font):
    """
    Generates images for every letters given in the array
    """
    global INDEX

    # define font
    font_path, font_size = font
    font = ImageFont.truetype(font_path, font_size)

    for letter,label in data.items():
        INDEX += 1
        # create a grayscale image
        img = Image.fromarray(FRAME)
        # get graphics
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), letter, 255, font=font)
        # trim image
        img = trim(img)
        # save image
        name = '{:05d}.png'.format(INDEX)
        save_to = os.path.join(OUTPUT_PATH, label)
        checkPath(save_to)
        img.save(os.path.join(save_to, name))
    # end for
# end function


def run():
    """
    To generate the image from the texts
    """
    for font in cfg.UNICODE_FONTS:
        generate(cfg.LETTER_LABELS, font)
        generate(cfg.NUMERAL_LABELS, font)
    # end for
# end if
