# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util


def process(img, region):
    """
    Extract plate regions    
    :param img: input image
    :param region: region data
    """

    x1, x2, y1, y2 = region
    plate = img[x1:x2, y1:y2]

    return plate
# end function


def run(prev, cur, scaled):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param scaled: Stage number for scaled gray image
    """
    util.log("Stage", cur, "Extracting plate from scaled image")
    for read in util.get_data(prev):
        # processed image from last stage
        region = util.stage_data(read, prev)
        region = np.load(region)

        # scaled image from 2nd stage
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, scaled)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        plate = process(img, region)

        # save plate
        write = util.stage_image(read, cur)
        cv2.imwrite(write, plate)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
