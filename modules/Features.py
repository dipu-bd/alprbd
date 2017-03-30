# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util


def process(img):
    """
    Extract 25 features plate regions    
    :param img: plate image 
    """
    height, width = img.shape

    # center of image
    cx = height // 2
    cy = width // 2

    feature = np.empty(25, dtype=float)
    total_pixels = height * width

    # 2 parts : horizontal
    up_pixels = np.count_nonzero(img[:cx, :])
    feature[0] = 100 * up_pixels / total_pixels

    down_pixels = np.count_nonzero(img[cx:, :])
    feature[1] = 100 * down_pixels / total_pixels

    # 2 parts : vertical
    left_pixels = np.count_nonzero(img[:, :cy])
    feature[2] = 100 * left_pixels / total_pixels

    right_pixels = np.count_nonzero(img[:, cy:])
    feature[3] = 100 * right_pixels / total_pixels

    # four parts
    up_left = np.count_nonzero(img[:cx, :cy])
    feature[4] = 100 * up_left / total_pixels

    down_left = np.count_nonzero(img[cx:, :cy])
    feature[5] = 100 * down_left / total_pixels

    up_right = np.count_nonzero(img[:cx, cy:])
    feature[6] = 100 * up_right / total_pixels

    down_right = np.count_nonzero(img[cx:, cy:])
    feature[7] = 100 * down_right / total_pixels

    # eight parts
    qx = height // 4
    qy = width // 4
    four = range(0, 4)
    for i in four:
        for j in four:
            x1 = i * qx
            x2 = (i + 1) * qx
            y1 = j * qy
            y2 = (j + 1) * qy

            pixels = np.count_nonzero(img[x1:x2, y1:y2])
            feature[8 + 4 * i + j] = 100 * pixels / total_pixels
        # end if
    # end if

    # 25th feature
    x, y = np.nonzero(img)
    dists = np.hypot(x - cx, y - cy)
    feature[24] = np.sum(dists)

    return feature
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    util.log("Stage", cur, "Crop the plate regions")
    util.delete_stage(cur)
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
