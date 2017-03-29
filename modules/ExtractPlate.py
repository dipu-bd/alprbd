# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def process(img):
    """
    Extract plate regions    
    :param img: input image
    :param matched: image after matched filter is applied
    """


# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Locate plate regions")
    for read in util.get_images(stage):
        # open image
        scaled = util.stage_image(read, 2)
        scaled = cv2.imread(scaled, cv2.CV_8UC1)
        region = util.stage_data(read, stage)
        region = cv2.imread(processed, cv2.CV_8UC1)

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
