# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def calculate(img):
    """
    Calculate the horizontal projections.
    :param img: plate image 
    """
    # calculate horizontal projections
    hor = horizontal(img)

    # calculate vertical projections
    segments = []
    for x in hor:
        segments.extend(vertical(x))
    # end for

    return segments
# end function


def horizontal(img):
    """
    Calculate the horizontal segments.
    :param img: plate image 
    """
    tmp = img.copy()
    tmp[tmp > 0] = 1

    row_sum = np.sum(tmp, axis=1)
    offset_min = np.mean(row_sum) / 2
    min_size = img.shape[0] // 10

    hor = []
    plate = None
    for r, v in enumerate(row_sum):
        if v > offset_min:
            if plate is None:
                plate = img[r:r + 1, :]
            else:
                plate = np.vstack((plate, img[r:r + 1, :]))
            # end if
        else:
            if isvalid(plate):
                hor.append(plate)
                plate = None
            # end if
        # end if
    # end for
    if isvalid(plate):
        hor.append(plate)
    # end if

    return hor
# end if


def vertical(img):
    """
    Calculate the horizontal segments.
    :param img: plate image 
    """
    tmp = img.copy()
    tmp[tmp > 0] = 1

    col_sum = np.sum(tmp, axis=0)
    offset_min = 2 * np.mean(col_sum) / 5
    min_size = 15

    ver = []
    plate = None
    for c, v in enumerate(col_sum):
        if v > offset_min:
            if plate is None:
                plate = img[:, c:c+1]
            else:
                plate = np.hstack((plate, img[:, c:c+1]))
            # end if
        else:
            if isvalid(plate):
                ver.append(plate)
                plate = None
            # end if
        # end if
    # end for
    if isvalid(plate):
        ver.append(plate)
    # end if

    return ver
# end if


def isvalid(plate):
    """
    Checks whether the plate is valid
    :param plate: 
    :return: 
    """
    if plate is None:
        return False
    # end if

    row, col = plate.shape
    if row < 20 or col < 20:
        return False
    # end if

    if np.count_nonzero(plate) < 100:
        return False
    # end if

    return True
# end if


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
        segments, time = util.execute_module(calculate, plate)
        runtime.append(time)

        # save all segments
        for idx, seg in enumerate(segments):
            write = util.stage_image(read, cur, idx)
            cv2.imwrite(write, seg)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
