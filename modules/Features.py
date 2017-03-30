# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util


def process(img):
    """
    Extract plate regions    
    :param img: plate image 
    """
    height, width = img.shape
    

# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    util.log("Stage", cur, "Crop the plate regions")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        data = process(plate)

        # save new region to data files
        write = util.stage_data(read, cur)
        np.save(write, data)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
