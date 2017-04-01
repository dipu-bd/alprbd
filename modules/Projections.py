# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def calculate(plate):
    """
    Calculate the horizontal projections.
    :param plate: plate image 
    """
    row, col = plate.shape

    # 1 Calculate horizontal projection
    row_sum = np.sum(plate, axis=1)
    row_mean = np.mean(row_sum)
    row_min = (row_mean + 2 * np.min(row_sum)) // 3
    min_size = row // 10

    # 2 Split rows and combine them
    combined = np.zeros((row, 2 * col))
    start, c, mxr = 0, 0, 0
    for i, v in enumerate(row_sum):
        if v > row_min:
            continue
        # end if
        if i - start > min_size and c < 2:
            x = max(0, start - 5)
            y = min(row, i + 5)
            combined[0:y - x, (c * col):((c + 1) * col)] = plate[x:y, :]
            mxr = max(mxr, y - x)
            c = (c + 1)
        # end if
        start = i
    # end for

    if row - start > min_size and c < 2:
        x = max(0, start - 5)
        y = min(row, row + 5)
        combined[0:y - x, (c * col):((c + 1) * col)] = plate[x:y, :]
        mxr = max(mxr, y - x)
        c = (c + 1)
    # end if
    if c == 0:
        return []
    # end if

    col *= c
    combined = combined[0:mxr, 0:col]

    col_sum = np.sum(combined, axis=0)
    col_mean = np.mean(col_sum)
    col_min = (col_mean + 4 * np.min(col_sum)) // 5
    col_max = (col_mean + 4 * np.max(col_sum)) // 5
    min_size = 10

    # 2 Split columns and combine them
    last = 0
    chars = []
    for i, v in enumerate(col_sum):
        if col_min < v < col_max:
            continue
        # end if
        if i - last > min_size:
            x = max(0, last - 2)
            y = min(row, i + 2)
            chars.append(combined[:, x:y])
        # end if
        last = i
    # end for
    if col - last > min_size:
        x = max(0, last - 2)
        y = min(row, col + 2)
        chars.append(combined[:, x:y])
    # end if

    return chars
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
