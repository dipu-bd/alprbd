# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(img, _pass=1):
    """
    Apply morphological operation
    :param img: input image
    :param _pass: iteration count
    """

    # build structuring element
    se = cv2.getStructuringElement(cv2.MORPH_RECT, cfg.MORPH_RECT_SIZE)

    # apply morphological erosion -- https://goo.gl/AuOAyL
    out = cv2.erode(img, se, iterations=_pass)

    return out
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Applying Erosion", 1, "pass")
    for read in util.get_images(stage):
        # open image
        file = util.stage_image(read, stage)
        img = cv2.imread(file, cv2.CV_8UC1)
        # apply
        out = apply(img)
        # save to file
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, out)
        # glass view
        file = util.stage_image(read, 8)
        img = cv2.imread(file, cv2.CV_8UC1)
        img[out < 250] = 0
        write = util.stage_image("." + read, stage + 1)
        cv2.imwrite(write, img)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
