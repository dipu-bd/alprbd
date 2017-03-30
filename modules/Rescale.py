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


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    util.log("Stage", cur, "Rescaling")
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
