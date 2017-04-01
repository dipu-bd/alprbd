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
    height, width = img.shape
    imgArea = height * width

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    regions = []
    for cnt in contours:
        # get bounding box
        y, x, col, row = cv2.boundingRect(cnt)

        # check height and width
        if row >= col or row < cfg.MIN_HEIGHT or col < cfg.MIN_WIDTH:
            continue
        # end if

        # check area
        area = row * col
        if area / imgArea < cfg.MIN_AREA:
            continue
        # end if

        # check aspect ratio
        aspect = row / col
        if aspect < cfg.MIN_ASPECT or aspect > cfg.MAX_ASPECT:
            continue
        # end if

        # minimum area box
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)

        # check rotation
        angle = abs(rect[2])
        if cfg.MAX_ANGLE < angle < 90 - cfg.MAX_ANGLE:
            continue
        # end if

        # draw the contour
        box = np.int32(box)
        cv2.drawContours(img, [box], 0, 255, 3)
        cv2.drawContours(img, [box], 0, 0, 2)

        # get region data
        center = [rect[0][0], rect[0][1]]
        size = [rect[1][0], rect[1][1]]
        region = [[x, y], [x+row, y+col], center, size, [rect[2], 0]]
        regions.append(region)
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
            write = util.stage_data(read, cur, index)
            np.savetxt(write, mat)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
