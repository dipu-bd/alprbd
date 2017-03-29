# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def process(img, region1, region2):
    """
    Extract original plate     
    :param img: original plate image
    :param region1: position relative to scaled
    :param region2: position relative to region1
    :return orignal plate image and region 
    """

    # translate to intermediate region
    x1, x2, y1, y2 = region2
    x, y = region1[0], region1[1]

    x1 += x
    x2 += x
    y1 += y
    y2 += y

    # translate points to original
    row, col = img.shape
    height, width = cfg.SCALE_DIM

    px, py = x1, y1
    x1 = int((px + x1) * row / height)
    x2 = int((px + x2) * row / height)
    y1 = int((py + y1) * col / width)
    y2 = int((py + y2) * col / width)

    # extract plate and regions
    plate = img[x1:x2, y1:y2]
    region = [x1, x2, y1, y2]

    return plate, region
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Crop the plate regions")
    for read in util.get_data(stage):
        # open scaled region data
        region1 = util.stage_data(read, 7)
        region1 = np.load(region1)
        # open relative region data
        region2 = util.stage_data(read, stage)
        region2 = np.load(region2)
        # get original image
        img = util.stage_image(read, 1)
        img = cv2.imread(img, cv2.CV_8UC1)
        # get result
        plate, region = process(img, region1, region2)
        # save plates to image files
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, plate)
        # save new region to data files
        write = util.stage_data(read, stage + 1)
        np.save(write, region)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
