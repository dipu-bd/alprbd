# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply_flood_fill(img, region, tx=0, ty=0):
    row, col = img.shape
    mask = np.zeros((row + 2, col + 2), np.uint8)
    for x, _ in enumerate(region):
        for y, c in enumerate(_):
            if c > 0:
                cv2.floodFill(img, mask, (ty+y, tx+x), 0)
            # end if
        # end if
    # end if
    return img
# end function


def calculate(img):
    """
    Remove borders.
    :param img: plate image 
    """
    row, col = img.shape
    img[img < 128] = 0
    img[img > 0] = 255

    # remove borders
    upper = img[0:10, :]
    lower = img[row-5:row, :]
    left = img[:, 0:5]
    right = img[:, col-5:col]

    img = apply_flood_fill(img, upper)
    img = apply_flood_fill(img, lower, tx=row-5)
    img = apply_flood_fill(img, left)
    img = apply_flood_fill(img, right, ty=col-5)

    return img
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Border removal")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(calculate, plate)
        runtime.append(time)

        # save output image
        if out is not None:
            write = util.stage_image(read, cur)
            cv2.imwrite(write, out)
        # end if

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
