# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def apply(img):
    """
    Converts to black and white    
    :param img: plate image 
    """

    # which type of threshold to apply
    _type = cv2.THRESH_BINARY_INV
    if np.mean(img) < 80:
        _type = cv2.THRESH_BINARY
    # end if

    # also apply Otsu's threshold
    _type = _type | cv2.THRESH_OTSU

    # applying threshold mixture
    bnw = cv2.threshold(np.uint8(img), cfg.BNW_THRESH, 255, _type)[1]

    return bnw
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Converts to black and white")
    for read in util.get_images(stage):
        # get plate from last stage
        plate = util.stage_image(read, stage)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        out = apply(plate)

        # save plates to image files
        if out is not None:
            write = util.stage_image(read, stage + 1)
            cv2.imwrite(write, out)
        # end if

        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
