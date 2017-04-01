# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(matched):
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
        y, x, n, m = cv2.boundingRect(cnt)

        # check image size and area
        if m >= n or m < 30 or n < 85\
                or m > 150 or n > 275:
            continue
        # end if

        # store values
        region = [x, x + n, y, y + m, n, m]
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
        (plates, regions), time = util.execute_module(process, matched)
        runtime.append(time)

        # save regions to data files
        for index, mat in enumerate(regions):
            name = "{}.{}".format(index, read)
            write = util.stage_data(name, cur)
            np.savetxt(write, mat)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
