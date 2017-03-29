# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def process(img, matched):
    """
    Extract plate regions    
    :param img: input image
    :param matched: image after matched filter is applied
    """

    plates = []
    regions = []
    H, W = cfg.SCALE_DIM
    minM, minN = cfg.MIN_PLATE_SIZE
    maxM, maxN = cfg.MAX_PLATE_SIZE

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    for cnt in contours:
        # get bounding box
        y, x, n, m = cv2.boundingRect(cnt)
        if m > n or (m < minM or n < minN) or (m > maxM or n > maxN):
            continue
        # end if

        # fix positions
        # x -= 5
        # m += 10
        # y -= 10
        # n += 20

        # get corner points
        x1 = max(0, x)
        x2 = min(H, x + m)
        y1 = max(0, y)
        y2 = min(W, y + n)

        # extract plate
        plate = img[x1:x2, y1:y2]

        # store values
        plates.append(plate)
        regions.append([x1, x2, y1, y2])
    # end for

    return plates, regions
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Locate plate regions")
    for read in util.get_images(stage):
        scaled = util.stage_image(read, 2)
        processed = util.stage_image(read, stage)
        # open image
        scaled = cv2.imread(scaled, cv2.CV_8UC1)
        processed = cv2.imread(processed, cv2.CV_8UC1)
        # get result
        plates, regions = process(scaled, processed)

        # save regions to data files
        for index, mat in enumerate(regions):
            name = "{}.{}".format(index, read)
            write = util.stage_image(name, stage + 1, True)
            np.save(write, mat)
        # end for

        # save plates to image files
        for index, plate in enumerate(plates):
            name = "{}.{}".format(index, read)
            write = util.stage_image(name, stage + 1)
            cv2.imwrite(write, plate)
        # end for

        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
