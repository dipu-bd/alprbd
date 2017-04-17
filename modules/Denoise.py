# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def apply(img):
    """
    Remove noise.
    :param img: plate image 
    """
    row, col = img.shape
    img[img < 128] = 0
    img[img > 0] = 255

    # de-noise using contours
    contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    for cnt in contours:
        y, x, n, m = cv2.boundingRect(cnt)
        if 35 < m < row - 25 and 35 < n < col - 25:
            continue
        # end if

        cv2.fillConvexPoly(img, cnt, 0)
        # rect = cv2.minAreaRect(cnt)
        # box = np.int32(cv2.boxPoints(rect))
        # cv2.fillConvexPoly(img, box, 0)
    # end for

    # check mean white pixels
    if np.mean(img) < 8:
        return None
    # end if

    return img
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Contour de-noising")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, plate)
        runtime.append(time)

        # save output image
        if out is not None:
            write = util.stage_image(read, cur)
            cv2.imwrite(write, out)
        # end if

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
