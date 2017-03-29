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


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Locate plate regions")
    for read in util.get_data(stage):
        # scaled image from 2nd stage
        name = ".".join(read.split(".")[1:])
        img = util.stage_image(name, 2)
        img = cv2.imread(img, cv2.CV_8UC1)
        # processed image from last stage
        region = util.stage_data(read, stage)
        region = np.load(region)
        # get result
        plate = process(img, region)
        # save plate
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, plate)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
