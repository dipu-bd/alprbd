# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def calculate(img):
    """
    Calculate the horizontal projections.
    :param img: plate image 
    """
    row, col = img.shape
    tmp = img.copy()
    tmp[tmp > 0] = 1

    row_sum = np.sum(tmp, axis=1)
    offset_min = np.mean(row_sum) / 2
    min_size = row // 10

    hor = []
    plate = None
    for r, v in enumerate(row_sum):
        if v > offset_min:
            if plate is None:
                plate = img[r:r+1, :]
            else:
                plate = np.vstack((plate, img[r:r+1, :]))
            # end if
        else:
            if plate is not None and plate.shape[0] > min_size:
                hor.append(plate)
                plate = None
            # end if
        # end if
    # end for
    if plate is not None:
        hor.append(plate)
    # end if

    return hor
# end function


def horizontal_segments(img):
    """
    Calculate the horizontal segments.
    :param img: plate image 
    """
    row, col = img.shape
    tmp = img.copy()
    tmp[tmp > 0] = 1

    row_sum = np.sum(tmp, axis=1)
    offset_min = np.mean(row_sum) / 2
    min_size = row // 10

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
            if plate is not None and plate.shape[0] > min_size:
                hor.append(plate)
                plate = None
                # end if
                # end if
    # end for
    if plate is not None:
        hor.append(plate)
    # end if

    return hor

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
