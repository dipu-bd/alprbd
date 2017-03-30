# -*- coding: utf-8 -*-

import cv2

from modules import Threshold
from modules import config as cfg
from modules import util


def apply(img):
    """
    Apply vertical Sobel operator
    :param img: input image 
    """

    # vertical Sobel operator -- https://goo.gl/3fQnc9
    sobel = cv2.Sobel(img, cv2.CV_8UC1, 1, 0, ksize=3)

    # apply custom threshold
    thresh = Threshold.apply(sobel, cfg.SOBEL_CUTOFF)

    # normalize image
    return thresh
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    util.log("Stage", cur, "Applying Sobel Operator")
    util.delete_stage(cur)
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # apply
        out = apply(img)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
