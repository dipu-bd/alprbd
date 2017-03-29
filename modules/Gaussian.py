# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg

blur_kernel = []


def apply(read, write):
    """
    Apply Gaussian blur
    :param read: input image file 
    :param write: output image file
    """

    # open image
    img = cv2.imread(read)

    # cv2 thresh -- https://goo.gl/OHjx6d

    # get the kernel
    kernel = build_blur_kernel()

    # apply 2D Gaussian filter -- https://goo.gl/jfuzjO
    gauss = cv2.filter2D(img, cv2.CV_64F, kernel)

    # normalize image
    out = util.normalize(gauss)

    # save to file
    cv2.imwrite(write, out)

    return out
# end function


def build_blur_kernel():
    """
    Build 2D Gaussian kernel 
    """

    global blur_kernel

    # check if it has already been calculated
    if blur_kernel.shape == cfg.BLUR_SIZE:
        return blur_kernel
    # end if

    # formula -- https://goo.gl/3AmmaE

    A = cfg.BLUR_COEFF
    m, n = cfg.BLUR_SIZE
    sx, sy = cfg.BLUR_SIGMA

    x0 = m / 2
    y0 = n / 2

    X = np.arange(m)
    Y = np.arange(n)

    X = np.square((X - x0) / sx)
    Y = np.square((Y - y0) / sy)

    Y, X = np.meshgrid(Y, X)
    blur_kernel = A * np.exp(-(X + Y) / 2)

    return blur_kernel
# end function
