# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import Threshold
from modules import config as cfg


def apply(read, write):
    """
    Apply vertical Sobel operator
    :param read: input image file 
    :param write: output image file
    """

    # open image
    img = cv2.imread(read)

    # vertical Sobel operator -- https://goo.gl/3fQnc9
    sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    # a low threshold
    thresh = Threshold.apply(sobel, cfg.SOBEL_CUTOFF)

    # normalize image
    out = util.normalize(thresh)

    # save to file
    cv2.imwrite(write, out)

    return  out
# end function
