# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(img):
    """
    Rescale image
    :param img: input image  
    """

    # build structuring element
    se = cv2.getStructuringElement(cv2.MORPH_RECT, cfg.MORPH_RECT_SIZE)

    # apply morphological dilation -- https://goo.gl/AuOAyL
    dilated = cv2.dilate(img, se, iterations=2)

    return dilated
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Applying Dilation")
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
