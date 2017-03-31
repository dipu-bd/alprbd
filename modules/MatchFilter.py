# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *
from modules import Gaussian
from modules import Sobel
from modules import Threshold

mixture_model = np.array([])


def apply(img, _all=False):
    """
    Apply matched filter using a mixture model
    :param img: enhanced image 
    :param _all: True to return all artifacts 
    """

    # apply sobel filter
    sobel = Sobel.apply(img)

    # apply matched filter
    kernel = _mixture_model()
    matched = cv2.filter2D(sobel, cv2.CV_64F, kernel)
    matched = util.normalize(matched)

    # smoothing by gaussian kernel
    smooth = Gaussian.apply(matched)

    # apply threshold
    thresh = Threshold.apply(np.uint8(smooth), cfg.SMOOTH_CUTOFF)

    # return all artifacts
    if _all:
        return sobel, matched, smooth, thresh
    else:
        return thresh
    # end if
# end function


def _mixture_model():
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
    A, B = cfg.MIXTURE_CO
    sx = cfg.MIXTURE_SIGMA

    a = m // 3
    b = 2 * m // 3

    x1 = m // 6
    x2 = a + m // 6
    x3 = b + m // 6

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


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Applying mixture model")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        results, time = util.execute_module(apply, img, True)
        sobel, matched, smooth, thresh = results
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, thresh)
        
        # ---## other artifacts ##--- #
        write = util.stage_image(".1." + read, cur)
        cv2.imwrite(write, matched)
        write = util.stage_image(".2." + read, cur)
        cv2.imwrite(write, smooth)
        # glass view
        img[thresh == 0] = 0
        write = util.stage_image(".3." + read, cur)
        cv2.imwrite(write, img)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
