"""
Generates basic dataset
"""
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import config as cfg
from Transformer import transform

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Necessary variables
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


def generate(data, font, index):
    """
    Generates images for every letters given in the array
    """    
    for letter, label in data.items():
        index += 1
        # create a grayscale image
        img = Image.fromarray(FRAME)
        # get graphics
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), letter, 255, font=font)
        # save image
        name = '{:04d}.bmp'.format(index)
        image_folder = os.path.join(OUTPUT_PATH, label)
        check_path(image_folder)
        image_file = os.path.join(image_folder, name)
        img.save(image_file)
        # trim image
        trim_image(image_file)
        # transform image
        index = transform(image_file, index)
    # end for
    return index
# end function


def run(index):
    """
    To generate the image from the texts
    """
    print("Generating numbers and letters...")
    for font_path, font_size in cfg.UNICODE_FONTS:
        font = ImageFont.truetype(font_path, font_size)
        index = generate(cfg.NUMERAL_LABELS, font, index)
        index = generate(cfg.LETTER_LABELS, font, index)
    # end for    
    return index
# end if
