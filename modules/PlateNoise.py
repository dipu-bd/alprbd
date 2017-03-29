# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import Gaussian
from modules import Threshold
from modules import config as cfg


def apply(img):
    """
    Apply a truncate-to-zero threshold
    :param img: input image 
    :param offset: Threshold offset 
    """

    # apply gaussian blur
    gauss = Gaussian.apply(img)

    # apply a threshold
    thresh = Threshold.apply(np.uint8(gauss), cfg.PLATE_OFFSET)

    return thresh
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Removing plate noises")
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
        file = util.stage_image(read, 7)
        img = cv2.imread(file, cv2.CV_8UC1)
        img[out < 250] = 0
        write = util.stage_image("." + read, stage + 1)
        cv2.imwrite(write, img)
        # log
        util.log("Converted", read, stage=stage)
    # end for
# end function
