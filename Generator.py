"""
Generates basic dataset
"""
# -*- coding: utf-8 -*-

import os
import cv2
import shutil
import numpy as np
import config as cfg
from Transformer import transform

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Necessary variables
FRAME = np.zeros([100, 300], dtype=np.uint8)

def check_path(output):
    """
    if a directory does not exists, creates it.
    """
    if not os.path.exists(output):
        os.makedirs(output)
    #end if
# end function


def get_name(index, save_path, label=None):
    name = '{:05d}.bmp'.format(index)
    if label is not None:
        folder = os.path.join(save_path, label)
    # end if
    check_path(folder)
    return os.path.join(folder, name)
# end function

def generate(data, font, index, save_path):
    """
    Generates images for every letters given in the array
    """    
    for letter in data:
        index += 1
        # create a grayscale image
        img = Image.fromarray(FRAME)
        # get graphics
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), letter, 255, font=font)
        # save image
        image_file = get_name(index, save_path, letter)
        img.save(image_file)
        # transform image
        index = transform(image_file, index)
    # end for
    return index
# end function


def copyfiles(files, index, save_path):
    """
    Copy all files to save_path and apply transformation
    """
    for file in files:
        index += 1
        # copy
        folder = os.path.splitext(file)[0]
        dst = get_name(index, folder)
        shutil.copyfile(file, dst)
        # transform
        index = transform(dst, index)
    # end for
    return index
# end function


def run():
    """
    To generate the image from the texts
    """
    index = 0
    print("Generating numbers and letters...")
    for font_path, font_size in cfg.UNICODE_FONTS:
        font = ImageFont.truetype(font_path, font_size)
        
        save_path = os.path.join(cfg.DIGITS_PATH, 'generated')
        index = generate(cfg.NUMERALS, font, index, save_path)

        save_path = os.path.join(cfg.LETTERS_PATH, 'generated')
        index = generate(cfg.LETTERS, font, index, save_path)

        save_path = os.path.join(cfg.CITY_PATH, 'generated')
        index = copyfiles(cfg.CITIES, index, save_path)
    # end for
    print("Generated %d images." % index)
# end if
