# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, region):
    """
    Extract original plate     
    :param img: original plate image
    :param region: position relative to scaled
    :return original plate image and region 
    """
    x1, x2, y1, y2 = np.uint(region)

    row, col = img.shape
    height, width = cfg.SCALE_DIM

    x1 = x1 * row // height
    x2 = x2 * row // height
    y1 = y1 * col // width
    y2 = y2 * col // width

    region = [x1, x2, y1, y2]
    return region
# end function


def run(prev, cur, gray):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param gray: Stage number of unscaled gray image
    """
    util.log("Stage", cur, "Translating to original points")
    util.delete_stage(cur)
    for read in util.get_data(prev):
        # open plate region data
        region = util.stage_data(read, prev)
        region = np.loadtxt(region)

        # get original image
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, gray)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        region = process(img, region)

        # save new region to data files
        write = util.stage_data(read, cur)
        np.save(write, region)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
