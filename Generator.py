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
outputPath = os.path.join('output', 'generated')


def checkPath(output):
    if not os.path.exists(output):
        os.makedirs(output)
    #end if
# end function


def trim(img):
    img_arr = np.array(img)
    rows, cols = img_arr.shape
    nzx, nzy = np.nonzero(img_arr)
    x1 = max(0, np.min(nzx) - 5)
    x2 = min(rows, np.max(nzx) + 5)
    y1 = max(0, np.min(nzy) - 5)
    y2 = min(cols, np.max(nzy) + 5)
    cropped = img_arr[x1:x2, y1:y2]
    return Image.fromarray(cropped)
# end function


def generate(array, font):
    """
    Generates images for every letters given in the array
    """
    global INDEX

    # define font
    font_path, font_size = font
    font = ImageFont.truetype(font_path, font_size)

    for letter in array:
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
        savePath = os.path.join(outputPath, name)
        img.save(savePath)
    # end for
# end function


def run():
    """
    To generate the image from the texts
    """
    for font in cfg.unicode_fonts:
        generate(cfg.letters, font)
        generate(cfg.numerals, font)
    # end for
    for font in cfg.bijoy_fonts:
        generate(cfg.strings, font)
    #end for
# end if
