# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, matched):
    """
    Locate plate regions
    :param img: scaled image 
    :param matched: image after matched filter is applied
    """
    # returnee variables
    plates = []
    regions = []

    # minimum settings
    min_m, min_n = cfg.MIN_PLATE_SIZE
    max_m, max_n = cfg.MAX_PLATE_SIZE
    min_area, max_area = cfg.PLATE_AREA

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    for cnt in contours:
        # get bounding box
        y, x, n, m = cv2.boundingRect(cnt)

        # check image size and area
        if m > n or (m < min_m or n < min_n)\
                or (m > max_m or n > max_n)\
                or (m * n < min_area)\
                or (m * n > max_area):
            continue
        # end if

        # get corner points
        x1 = x
        x2 = x + m
        y1 = y
        y2 = y + n

        # store values
        plate = img[x1:x2, y1:y2]
        plates.append(plate)

        region = [x1, x2, y1, y2]
        regions.append(region)
    # end for

    return plates, regions
# end function


def run(prev, cur, original):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param original: Stage number for original image
    """
    runtime = []
    util.log("Stage", cur, "Locate plate regions")
    for read in util.get_images(prev):
        # processed image from last stage
        matched = util.stage_image(read, prev)
        matched = cv2.imread(matched, cv2.CV_8UC1)

        # original image
        img = util.stage_image(read, original)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        (plates, regions), time = util.execute_module(process, img, matched)
        runtime.append(time)

        # save regions to data files
        for index, mat in enumerate(regions):
            name = "{}.{}".format(index, read)
            write = util.stage_data(name, cur)
            np.savetxt(write, mat)
        # end for

        # save plates to image files
        for index, mat in enumerate(plates):
            name = "{}.{}".format(index, read)
            write = util.stage_image(name, cur)
            cv2.imwrite(write, mat)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
