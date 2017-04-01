# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply(img):
    """
    Converts to black and white    
    :param img: plate image 
    """
    # normal binary threshold
    bnw1 = cv2.threshold(np.uint8(img), cfg.BNW_THRESH, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # inverse binary threshold
    bnw2 = cv2.threshold(np.uint8(img), cfg.BNW_THRESH, 255,
                         cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # calculate ratio of non-zero pixels
    row, col = img.shape
    area = row * col
    ratio1 = cv2.countNonZero(bnw1) / area
    ratio2 = cv2.countNonZero(bnw2) / area

    # return image with lower ratio
    if ratio1 < ratio2:
        return bnw1
    else:
        return bnw2
    # end if
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Converts to black and white")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, plate)
        runtime.append(time)

        # save plates to image files
        if out is not None:
            write = util.stage_image(read, cur)
            cv2.imwrite(write, out)
        # end if

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
