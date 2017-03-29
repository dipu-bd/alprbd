# -*- coding: utf-8 -*-

import cv2
from modules import config as cfg


def apply(read, write):
    """
    Rescale image
    :param read: input image file 
    :param write: output image file
    """

    # open image
    img = cv2.imread(read)

    # Rescale dimension
    h, w = cfg.SCALE_DIM

    # rescale image -- https://goo.gl/I9b3Ms
    out = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

    # save to file
    cv2.imwrite(write, out)

# end function
