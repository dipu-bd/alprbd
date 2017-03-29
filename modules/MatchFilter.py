# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import Sobel
from modules import Gaussian
from modules import config as cfg

mixture_model = np.array([])


def apply(img, all=None):
    """
    Apply vertical Sobel operator
    :param img: enhanced image 
    """

    # apply sobel filter
    sobel = Sobel.apply(img)

    # apply matched filter
    kernel = build_mixture_model()
    matched = cv2.filter2D(sobel, cv2.CV_8UC1, kernel)

    # smoothing by gaussian kernel
    smooth = Gaussian.apply(matched)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(smooth, cfg.SMOOTH_CUTOFF,
                              255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # normalize image
    return util.normalize(thresh)
# end function


def build_mixture_model():
    """
    Builds a gaussian kernel for mixture model
    """

    global mixture_model

    # check if it has already been calculated
    if mixture_model.shape == cfg.MIXTURE_SIZE:
        return mixture_model
    # end if

    # formula -- see paper

    m, n = cfg.MIXTURE_SIZE
    A, B = cfg.MIXTURE_COEFF
    sx, sy = cfg.MIXTURE_SIGMA

    a = int(m / 3)
    b = 2 * int(m / 3)

    x1 = int(m / 6)
    x2 = a + int(m / 6)
    x3 = b + int(m / 6)

    X = np.arange(m)
    Y = np.arange(n)

    X1 = X[:a]
    X2 = X[a:b]
    X3 = X[b:]

    X1 = np.square((X1 - x1) / sx)
    X2 = np.square((X2 - x2) / sx)
    X3 = np.square((X3 - x3) / sx)

    H1 = A * np.exp(-X1 / 0.2)
    H2 = B * np.exp(-X2 / 2.0)
    H3 = A * np.exp(-X3 / 0.2)
    H = np.hstack((H1, H2, H3))

    _, mixture_model = np.meshgrid(Y, H)
    return mixture_model
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Applying mixture model")
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
