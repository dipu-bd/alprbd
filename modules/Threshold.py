# -*- coding: utf-8 -*-

import cv2
from modules import util


def apply(img, offset=127):
    """
    Apply a truncate-to-zero threshold
    :param img: input image 
    :param offset: Threshold offset 
    """

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(img, offset, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :param stage: Threshold amount 
    :return: 
    """
    util.log("Stage", stage, "Applying threshold")
    for read in util.get_images(stage):
        # open image
        file = util.stage_image(read, stage)
        img = cv2.imread(file, cv2.CV_8UC1)

        # apply
        out = apply(img)

        # save to file
        write = util.stage_image(read, stage + 1)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, stage=stage)
    # end for
# end function
