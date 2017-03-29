# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg

blur_kernel = np.array([])


def apply(img):
    """
    Apply Gaussian blur
    :param img: input image 
    """

    # cv2 thresh -- https://goo.gl/OHjx6d

    # get the kernel
    kernel = build_blur_kernel()

    # apply 2D Gaussian filter -- https://goo.gl/jfuzjO
    gauss = cv2.filter2D(img, cv2.CV_8UC1, kernel)

    return gauss
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

    A = cfg.BLUR_COE
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


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Gaussian conversion")
    for read in util.get_images(stage):
        file = util.stage_file(read, stage)
        # open image
        img = cv2.imread(file, cv2.CV_8UC1)
        out = apply(img)
        # save to file
        write = util.stage_file(read, stage + 1)
        cv2.imwrite(write, out)
        # log
        util.log("Converted", read, stage=stage)
    # end for

# end function

