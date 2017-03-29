# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def process(matched):
    """
    Extract plate regions
    :param matched: image after matched filter is applied
    """

    plates = []
    regions = []
    height, width = cfg.SCALE_DIM
    min_m, min_n = cfg.MIN_PLATE_SIZE
    max_m, max_n = cfg.MAX_PLATE_SIZE

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    for cnt in contours:
        # get bounding box
        y, x, n, m = cv2.boundingRect(cnt)
        if m > n or (m < min_m or n < min_n) or (m > max_m or n > max_n):
            continue
        # end if

        # fix positions
        # x -= 5
        # m += 10
        # y -= 10
        # n += 20

        # get corner points
        x1 = max(0, x)
        x2 = min(height, x + m)
        y1 = max(0, y)
        y2 = min(width, y + n)

        # store values
        regions.append([x1, x2, y1, y2])
    # end for

    return plates, regions
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    """
    util.log("Stage", stage, "Locate plate regions")
    for read in util.get_images(stage):
        # processed image from last stage
        matched = util.stage_image(read, stage)
        matched = cv2.imread(matched, cv2.CV_8UC1)
        # get result
        plates, regions = process(matched)
        # save regions to data files
        for index, mat in enumerate(regions):
            name = "{}.{}".format(index, read)
            write = util.stage_data(name, stage + 1)
            np.save(write, mat)
        # end for

        # log
        util.log("Converted", read, stage=stage)
    # end for
# end function
