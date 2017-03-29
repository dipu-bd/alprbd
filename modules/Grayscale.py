# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(img):
    """
    Apply Gray-scale conversion
    :param img: input image file 
    """

    # split image parts
    b, g, r = cv2.split(img)

    # join parts using a ratio
    r = cfg.GRAY_RATIO[0] * r
    g = cfg.GRAY_RATIO[1] * g
    b = cfg.GRAY_RATIO[2] * b

    # to gray
    gray = r + g + b

    # normalize image
    out = util.normalize(gray)

    return out
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Grayscale conversion")
    for read in util.get_images(stage):
        file = util.stage_file(read, stage)
        # open image
        img = cv2.imread(file)
        out = apply(img)
        # save to file
        write = util.stage_file(read, stage + 1)
        cv2.imwrite(write, out)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
