# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply(img, _iter=1):
    """
    Apply dilation
    :param img: input image
    :param _iter: iteration count
    """

    # build structuring element
    se = cv2.getStructuringElement(cv2.MORPH_RECT, cfg.MORPH_RECT_SIZE)

    # apply morphological erosion -- https://goo.gl/AuOAyL
    out = cv2.dilate(img, se, iterations=_iter)

    return out
# end function


def run(prev, cur, _iter=1):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param _iter: iteration count
    """
    runtime = []
    util.log("Stage", cur, "Dilation")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, img, _iter)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function

