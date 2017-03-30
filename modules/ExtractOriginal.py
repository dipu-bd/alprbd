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
    :return original plate image and region 
    """
    # translate to scaled region
    x1, x2, y1, y2 = region2
    x = region1[0]
    y = region1[2]

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


def run(prev, cur, plate_region, gray):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param plate_region: Stage index of plate region data
    :param gray: Stage number of unscaled gray image
    """
    util.log("Stage", cur, "Extracting the plate from full sized image")
    for read in util.get_data(prev):
        # open relative region data
        region2 = util.stage_data(read, prev)
        region2 = np.load(region2)

        # open scaled region data
        name = ".".join(read.split(".")[1:])
        region1 = util.stage_data(name, plate_region)
        region1 = np.load(region1)

        # get original image
        name = ".".join(read.split(".")[2:])
        img = util.stage_image(name, gray)
        img = cv2.imread(img, cv2.CV_8UC1)

        # get result
        plate, region = process(img, region1, region2)

        # save plates to image files
        write = util.stage_image(read, cur)
        cv2.imwrite(write, plate)

        # save new region to data files
        write = util.stage_data(read, cur)
        np.save(write, region)

        # log
        util.log("Converted", read, stage=cur)
    # end for
# end function
