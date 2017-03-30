# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, region):
    """
    Extract plate regions    
    :param img: plate image
    :param region: position of the image
    :return cropped plate image and region 
    """

    return img, region
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Crop the plate regions")
    for read in util.get_images(stage):
        # open plate region data
        region = util.stage_data(read, 7)
        region = np.load(region)
        # get plate from last stage
        plate = util.stage_image(read, stage)
        plate = cv2.imread(plate, cv2.CV_8UC1)
        # get result
        plate, region = process(plate, region)
        # save new region to data files
        write = util.stage_data(read, stage + 1)
        np.save(write, region)
        # save plates to image files
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, plate)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
