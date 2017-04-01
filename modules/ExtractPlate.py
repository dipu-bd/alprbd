# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, region1, region2):
    """
    Extract original plate     
    :param img: original plate image
    :param region1: position relative to scaled
    :param region2: position relative to region1
    :return original plate image and region 
    """
    # translate to scaled region
    x1, x2, y1, y2 = np.uint(region2)
    x = int(region1[0])
    y = int(region1[2])

    x1 += x
    x2 += x
    y1 += y
    y2 += y

    # translate scaled to original
    row, col = img.shape
    height, width = cfg.SCALE_DIM

    x1 = int(x1 * row / height)
    x2 = int(x2 * row / height)
    y1 = int(y1 * col / width)
    y2 = int(y2 * col / width)

    # extract plate and regions
    plate = img[x1:x2, y1:y2]
    region = [x1, x2, y1, y2]

    return plate, region
# end function


def run(prev, cur, plate):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param plate: Stage number of plate image
    """
    runtime = []
    util.log("Stage", cur, "Extracting the plate image")
    for read in util.get_data(prev):
        # region data from the previous stage
        region = util.stage_data(read, prev)
        region = np.loadtxt(region)

        # get original image
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, plate)
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
