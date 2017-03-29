# -*- coding: utf-8 -*-

import cv2
from modules import util
from modules import config as cfg


def apply(read):
    """
    Apply Gray-scale conversion
    :param read: input image file 
    """

    util.log(read)

    # open image
    img = cv2.imread(read)

    # split image parts
    b, g, r = cv2.split(img)

    # join parts using a ratio
    r = cfg.GRAY_RATIO[0] * r
    g = cfg.GRAY_RATIO[1] * g
    b = cfg.GRAY_RATIO[2] * b

    # to gray
    gray = r + g + b

    # normalize image
    out = util.normalize(gray)

    # save to file
    write = util.get_file(out)
    cv2.imwrite(write, out)

    return out
# end function


def run(stage_no)



# end function