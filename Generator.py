"""
Generates basic dataset
"""
# -*- coding: utf-8 -*-

import os
import shutil
from glob import glob

import cv2
import numpy as np
import config as cfg
from Transformer import transform, normalize_image

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


def get_name(index, save_path, label):
    name = '{:05d}.bmp'.format(index)
    save_path = os.path.join(save_path, label)
    check_path(save_path)
    return os.path.join(save_path, name)
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


def generate_cities(index, save_path):
    """
    Copy all files to save_path and apply transformation
    """
    for file in glob('city/*.bmp'):
        index += 1
        # copy
        label = os.path.splitext(os.path.basename(file))[0]
        dst = get_name(index, save_path, label)
        shutil.copyfile(file, dst)
        # transform
        index = transform(dst, index)
    # end for
    return index
# end function


def generate_letters(index, save_path):
    """
    Copy all files to save_path and apply transformation
    """
    for file in glob('letters/**/*.bmp'):
        index += 1
        # copy
        label = file.split(os.sep)[-2]
        img = cv2.imread(file, 0)
        # end if
        dst = get_name(index, save_path, label)
        cv2.imwrite(dst, img)
        # transform
        normalize_image(dst, (28, 28))
        #index = transform(dst, index)
    # end for
    return index
# end function

def run():
    """
    To generate the image from the texts
    """
    index = 0
    for font_path, font_size in cfg.UNICODE_FONTS:
        font = ImageFont.truetype(font_path, font_size)
        
        print("Generating numbers... ", index)
        save_path = os.path.join(cfg.DIGITS_PATH, 'generated')
        index = generate(cfg.NUMERALS, font, index, save_path)
        
        print("Generating letters... ", index)
        save_path = os.path.join(cfg.LETTERS_PATH, 'generated')
        index = generate(cfg.LETTERS, font, index, save_path)
    # end for

    print("Generating cities...  ", index)
    save_path = os.path.join(cfg.CITY_PATH, 'generated')
    index = generate_cities(index, save_path)

    print("Generating more letters... ", index)
    save_path = os.path.join(cfg.LETTERS_PATH, 'generated')
    index = generate_letters(index, save_path)

    print("Generated %d images." % index)
# end if

