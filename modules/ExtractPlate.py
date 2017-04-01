# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, region):
    """
    Extract plate regions    
    :param img: input image
    :param region: region data
    """

    row, col = cfg.SCALE_DIM
    height, width = img.shape

    region = np.uint(region)

    x1 = region[0]
    x2 = region[1]
    y1 = region[2]
    y2 = region[3]

    x1 = x1 * height // row
    x2 = x2 * height // row
    y1 = y1 * width // col
    y2 = y2 * width // col

    return img[x1:x2, y1:y2]
# end function


def run(prev, cur, full):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param full: Stage number of full scaled gray image
    """
    runtime = []
    util.log("Stage", cur, "Extracting plates")
    for read in util.get_data(prev):
        # processed image from last stage
        region = util.stage_data(read, prev)
        region = np.loadtxt(region)

        # scaled image from 2nd stage
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, full)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        plate, time = util.execute_module(process, img, region)
        runtime.append(time)

        # save plate
        write = util.stage_image(read, cur)
        cv2.imwrite(write, plate)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
