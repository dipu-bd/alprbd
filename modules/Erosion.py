# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(img, _pass=1):
    """
    Apply dilation
    :param img: input image
    :param _pass: iteration count
    """

    # build structuring element
    se = cv2.getStructuringElement(cv2.MORPH_RECT, cfg.MORPH_RECT_SIZE)

    # apply morphological erosion
    out = cv2.erode(img, se, iterations=_pass)

    return out
# end function


def run(prev, cur, _pass):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param _pass: How many times to apply
    """
    util.log("Stage", prev, "Applying Erosion:", _pass, "pass")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # apply
        out = apply(img, _pass)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
