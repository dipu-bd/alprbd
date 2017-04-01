# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *
from modules import Threshold


def apply(img):
    """
    Apply vertical Sobel operator
    :param img: input image 
    """

    # vertical Sobel operator -- https://goo.gl/3fQnc9
    canny = cv2.Canny(img, 100, 200, L2gradient=True)

    # normalize image
    return canny
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Canny edge detection")
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
