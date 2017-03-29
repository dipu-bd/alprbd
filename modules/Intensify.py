# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules import util
from modules import config as cfg


def apply(img, gauss):
    """
    Intensify image around plate-like regions 
    :param img: scaled image
    :param gauss: gaussian image
    """

    m, n = cfg.BLOCK_COUNT
    row, col = img.shape
    h = int(row / m)
    w = int(col / n)

    x, y = np.ogrid[0:1:(1.0 / h), 0:1:(1.0 / w)]

    # loop iterators
    winX, winY = np.ogrid[0:row:h, 0:col:w]
    winX = winX.flatten()
    winY = winY.flatten()

    # gX, gY = np.ogrid[0:row:h, 0:col:w]

    mean = np.zeros((row, col), dtype=np.float64)
    sdev = np.zeros((row, col), dtype=np.float64)

    # for all windows
    for i in winX:
        for j in winY:
            # local average of four corners
            iA, dA = local_mean_std(gauss, i, j, h, w)
            iB, dB = local_mean_std(gauss, i, j + w, h, w)
            iC, dC = local_mean_std(gauss, i + h, j, h, w)
            iD, dD = local_mean_std(gauss, i + h, j + w, h, w)
            # calculate local intensity
            upperL = (1 - y) * iA + y * iB
            lowerL = (1 - y) * iC + y * iD
            mean[i:i + h, j:j + w] = np.dot(1 - x, upperL) + np.dot(x, lowerL)
            # calculate local standard deviation
            upperD = (1 - y) * dA + y * dB
            lowerD = (1 - y) * dC + y * dD
            sdev[i:i + h, j:j + w] = np.dot(1 - x, upperD) + np.dot(x, lowerD)
            # end for j
    # end for i

    # apply intensify
    f = np.vectorize(weight)
    ret = f(sdev) * (img - mean) + mean

    return util.normalize(ret)

# end function


def local_mean_std(img, i, j, p, q):
    """
    Calculates the mean intensity and standard deviation of a point
    :param img: Original image
    :param i: current row
    :param j: current column
    :param p: window height
    :param q: window width
    """
    row, col = img.shape

    # get window
    x1 = int(max(0, i - int(p / 2)))
    y1 = int(max(0, j - int(q / 2)))
    x2 = int(min(row, i + int(p / 2)))
    y2 = int(min(col, j + int(q / 2)))
    W = img[x1:x2, y1:y2]

    # calculate mean and std
    mean = np.mean(W)
    std = np.std(W / 255.0)
    return (mean, std)
# end function


def weight(rho):
    """The weighting function

    Parameter:
        rho -- The deviation at current pixel
    """
    a, b = cfg.WEIGHT_DIST
    t = (rho - a) ** 2

    w = 1.0
    if rho < a:
        p = 2 / (a ** 2)
        w = 3.0 / (p * t + 1)
    elif rho < b:
        q = 2 / ((b - a) ** 2)
        w = 3.0 / (q * t + 1)
    else:
        w = 1.0
    # end if

    return w
# end function


def run(stage):
    """
    Run stage task
    :param stage: Stage number 
    :return: 
    """
    util.log("Stage", stage, "Intensity distribution")
    for read in util.get_images(stage):
        gray = util.stage_file(read, 2)
        gauss = util.stage_file(read, stage)
        # open image
        gray = cv2.imread(gray, cv2.CV_8UC1)
        gauss = cv2.imread(gauss, cv2.CV_8UC1)
        # apply
        out = apply(gray, gauss)
        # save to file
        write = util.stage_file(read, stage + 1)
        cv2.imwrite(write, out)
        # log
        util.log("Converted", read, stage=stage)
    # end for
# end function
