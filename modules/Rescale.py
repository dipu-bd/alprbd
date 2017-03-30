# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


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
    runtime = []
    util.log("Stage", cur, "Rescaling")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, img)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
