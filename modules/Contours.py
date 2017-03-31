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
    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    regions = []
    for cnt in contours:
        # get bounding box
        bound = cv2.boundingRect(cnt)
        y, x, n, m = bound

        # check height and width
        if m >= n or m < cfg.MIN_HEIGHT\
                or m > cfg.MAX_HEIGHT\
                or n < cfg.MIN_WIDTH\
                or n > cfg.MAX_WIDTH:
            continue
        # end if

        # check area
        if m * n < cfg.MIN_AREA or m * n > cfg.MAX_AREA:
            continue
        # end if

        # check aspect ratio
        if m / n < cfg.MIN_ASPECT or m / n > cfg.MAX_ASPECT:
            continue
        # end if

        # minimum rectangle
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        A = box[0][0], box[0][1]
        B = box[1][0], box[1][1]
        C = box[2][0], box[2][1]
        D = box[3][0], box[3][1]

        # draw selected contour
        cv2.line(img, A, B, 255, thickness=4)
        cv2.line(img, B, C, 255, thickness=4)
        cv2.line(img, C, D, 255, thickness=4)
        cv2.line(img, D, A, 255, thickness=4)
        cv2.line(img, A, B, 0, thickness=2)
        cv2.line(img, B, C, 0, thickness=2)
        cv2.line(img, C, D, 0, thickness=2)
        cv2.line(img, D, A, 0, thickness=2)

        # get region data
        regions.append(box)
    # end for

    return regions
# end function


def run(prev, cur, original):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param original: Stage number for original image
    """
    runtime = []
    util.log("Stage", cur, "Contour analysis")
    for read in util.get_images(prev):
        # processed image from last stage
        matched = util.stage_image(read, prev)
        matched = cv2.imread(matched, cv2.CV_8UC1)

        # original image
        img = util.stage_image(read, original)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        regions, time = util.execute_module(process, img, matched)
        runtime.append(time)

        # save image with contours
        write = util.stage_image(read, cur)
        cv2.imwrite(write, img)

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
