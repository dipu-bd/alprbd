# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def run(stage, stage1, stage2):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage1, "Applying glass with Stage", stage2)
    for read in util.get_images(stage1):
        img = util.stage_file(read, stage2)
        cur = util.stage_file(read, stage1)
        # open image
        img = cv2.imread(img, cv2.CV_8UC1)
        cur = cv2.imread(cur, cv2.CV_8UC1)
        # glass
        img[cur < 250] = 0
        # save to file
        write = util.stage_file(read, stage + 1)
        cv2.imwrite(write, img)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function
