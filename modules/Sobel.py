# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import Threshold
from modules import config as cfg


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


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Applying Sobel Operator")
    for read in util.get_images(stage):
        # open image
        file = util.stage_image(read, stage)
        img = cv2.imread(file, cv2.CV_8UC1)

        # apply
        out = apply(img)

        # save to file
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, stage=stage)
    # end for
# end function
