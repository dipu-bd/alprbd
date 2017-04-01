# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply_flood_fill(img, region, tx, ty):
    row, col = img.shape
    mask = np.zeros((row + 2, col + 2), np.uint8)
    for x, _ in enumerate(region):
        for y, c in enumerate(_):
            if c > 0:
                cv2.floodFill(img, mask, (ty+y, tx+x), 0)
            # end if
        # end if
    # end if
# end function


def calculate(img):
    """
    Remove borders.
    :param img: plate image 
    """
    row, col = img.shape
    rd = 7
    cd = 7

    upper = img[0:rd, :]
    apply_flood_fill(img, upper, 0, 0)

    lower = img[row-rd:row, :]
    apply_flood_fill(img, lower, row-rd, 0)

    left = img[:, 0:cd]
    apply_flood_fill(img, left, 0, 0)

    right = img[:, col-cd:col]
    apply_flood_fill(img, right, 0, col-cd)

    return img
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Remove Border noise")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(calculate, plate)
        runtime.append(time)

        # save output image
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
