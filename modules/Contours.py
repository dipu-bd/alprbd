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
        y, x, m, n = bound

        # check height and width
        if n >= m or n < cfg.MIN_HEIGHT\
                or n > cfg.MAX_HEIGHT\
                or m < cfg.MIN_WIDTH\
                or m > cfg.MAX_WIDTH:
            continue
        # end if

        # check area
        if n * m < cfg.MIN_AREA or n * m > cfg.MAX_AREA:
            continue
        # end if

        # check aspect ratio
        if n / m < cfg.MIN_ASPECT or n / m > cfg.MAX_ASPECT:
            pass
            #continue
        # end if

        # check rotation ++++
        angle = cv2.minAreaRect(cnt)[2]
        if cfg.MAX_ANGLE < angle < 90 - cfg.MAX_ANGLE:
            pass
            #continue
        # end if

        # draw the contour
        cv2.rectangle(img, (x, y), (x+m, y+n), 255, thickness=3)
        cv2.rectangle(img, (x, y), (x+m, y+n), 0, thickness=2)

        # get region data
        box = [x, x + m, y, y + n]
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
