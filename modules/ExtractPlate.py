# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, region):
    """
    Extract original plate     
    :param img: original plate image
    :param region: region information
    """
    # extract plate
    x1, y1 = np.uint(region[0])
    x2, y2 = np.uint(region[1])
    plate = img[x1:x2, y1:y2]

    # calculate rotation angle
    angle = abs(region[4][0])
    if angle < 45:
        angle = -angle
    else:
        angle = 90 - angle
    # end if

    # rotate plate
    cy, cx = region[2]
    cols = y2 - y1
    rows = x2 - x1
    rot_mat = cv2.getRotationMatrix2D((cy, cx), angle, 1)
    out = cv2.warpAffine(plate, rot_mat, (cols, rows))

    return out
# end function


def run(prev, cur, original):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param original: Stage number of plate image
    """
    runtime = []
    util.log("Stage", cur, "Extracting the plate image")
    for read in util.get_data(prev):
        # region data from the previous stage
        region = util.stage_data(read, prev)
        region = np.loadtxt(region)

        # get original image
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, original)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        plate, time = util.execute_module(process, img, region)
        runtime.append(time)

        # save plates to image file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, plate)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
