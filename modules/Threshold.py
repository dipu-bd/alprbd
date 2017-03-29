# -*- coding: utf-8 -*-

import numpy as np


def apply(img, cutoff=0.3):
    """
    Apply a truncate-to-zero threshold
    :param img: input image 
    :param cutoff: cutoff point 
    """

    # cv2 thresh -- https://goo.gl/OHjx6d

    # my thresh
    cutoff *= np.max(img) - np.min(img)
    thresh = img.copy()
    thresh[thresh <= cutoff] = 0

    return thresh
# end function
