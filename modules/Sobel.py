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
    sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    # a low threshold
    thresh = Threshold.apply(sobel, cfg.SOBEL_CUTOFF)

    # normalize image
    return util.normalize(thresh)
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Applying Sobel Operator")
    for read in util.get_images(stage):
        file = util.stage_file(read, stage)
        # open image
        img = cv2.imread(file)
        out = apply(img)
        # save to file
        write = util.stage_file(read, stage + 1)
        cv2.imwrite(write, out)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
