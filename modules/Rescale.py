# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(img):
    """
    Rescale image
    :param img: input image  
    """

    # Rescale dimension
    h, w = cfg.SCALE_DIM

    # rescale image -- https://goo.gl/I9b3Ms
    out = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

    return out
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Rescaling")
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
