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
    return img
# end function


def calculate(img):
    """
    Remove borders.
    :param img: plate image 
    """
    # remove borders
    d = 10
    row, col = img.shape

    upper = img[0:d, :]
    img = apply_flood_fill(img, upper, 0, 0)

    lower = img[row-d:row, :]
    img = apply_flood_fill(img, lower, row-d, 0)

    left = img[:, 0:d]
    img = apply_flood_fill(img, left, 0, 0)

    right = img[:, col-d:col]
    img = apply_flood_fill(img, right, 0, col-d)

    # remove remaining noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # img = cv2.morphologyEx(img, cv2.MORPH_ELLIPSE, kernel)
    img = cv2.dilate(img, kernel)
    img = cv2.erode(img, kernel)

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
