# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


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


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Grayscale conversion")
    for read in util.get_images(prev):
        # open image
        img = util.stage_image(read, prev)
        img = cv2.imread(img)

        # get result
        out, time = util.execute_module(apply, img)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
