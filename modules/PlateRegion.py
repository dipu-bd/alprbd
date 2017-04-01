# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def locate(matched):
    """
    Locate plate regions
    :param matched: image after matched filter is applied
    """
    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    regions = []
    for cnt in contours:
        # get bounding box
        y, x, col, row = cv2.boundingRect(cnt)

        # check image size and area
        if row >= col or row < 30 or col < 85\
                or row > 150 or col > 275:
            continue
        # end if

        # store values
        region = [x, x + row, y, y + col, row, col]
        regions.append(region)
    # end for

    return regions
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Locate plate regions")
    for read in util.get_images(prev):
        # processed image from last stage
        matched = util.stage_image(read, prev)
        matched = cv2.imread(matched, cv2.CV_8UC1)

        # get result
        regions, time = util.execute_module(locate, matched)
        runtime.append(time)

        # save regions to data files
        for index, mat in enumerate(regions):
            write = util.stage_data(read, cur, index)
            np.savetxt(write, mat)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
