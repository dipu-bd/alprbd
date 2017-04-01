# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply(img, offset=50):
    """
    Apply a truncate-to-zero threshold
    :param img: input image 
    :param offset: Threshold offset 
    """

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(img, offset, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
# end function


def run(prev, cur, thresh=0):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param thresh: Threshold value to apply
    """
    runtime = []
    util.log("Stage", cur, "Applying threshold")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, img, thresh)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
