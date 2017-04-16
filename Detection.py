# -*- coding: utf-8 -*-

import cv2
import numpy as np
from os import path
import config as cfg


def detect(img):
    # necessary constants
    col, row = cfg.SCALE_DIM
    height, width, _ = img.shape

    # enhance
    enhanced = enhance(img)

    # matched filter
    matched = matched_filter(enhanced)

    # locate all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract clean plates
    plates = []
    for cnt in contours:
        # get bounding box
        y, x, c, r = cv2.boundingRect(cnt)

        # check image size 
        if not (r < c and 30 < r < 150 and 100 < c < 350):
            continue
        # end if

        # translate points
        x1 = x * height // row
        x2 = (x + r) * height // row
        y1 = y * width // col
        y2 = (y + c) * width // col

        # original ROI
        plate = grayscale(img[x1:x2, y1:y2])        
        plates.append(plate)
    # end for

    return plates
# end function


#####################################################################################
# --------------------------- 1st Level Functions --------------------------------- #
#####################################################################################


def grayscale(img):
    # grayscale 
    b, g, r = cv2.split(img)
    gray = cfg.GRAY_RATIO[0] * r + cfg.GRAY_RATIO[1] * g + cfg.GRAY_RATIO[2] * b    
    return normalize(gray)
# end function


def enhance(img):
    # rescale
    scaled = cv2.resize(img, cfg.SCALE_DIM, interpolation=cv2.INTER_AREA)

    # to grayscale
    gray = grayscale(scaled)

    # vertical Sobel operator -- https://goo.gl/3fQnc9
    sobel = cv2.Sobel(gray, cv2.CV_8UC1, 1, 0, ksize=3)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(sobel, cfg.SOBEL_CUTOFF, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # apply gaussian blur
    kernel = blur_kernel()
    gauss = cv2.filter2D(thresh, cv2.CV_64F, kernel)

    # calculate mean intensity and standard deviation
    row, col = thresh.shape
    mean, sdev = intensity_calculate(row, col, gauss)

    # intensify image
    f = np.vectorize(weight)
    ret = f(sdev) * (gray - mean) + mean

    # normalize and return 
    return normalize(ret)
# end function


def matched_filter(img): 
    # vertical Sobel operator -- https://goo.gl/3fQnc9
    sobel = cv2.Sobel(img, cv2.CV_8UC1, 1, 0, ksize=3)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(sobel, cfg.SOBEL_CUTOFF, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # apply matched filter
    kernel = mixture_model()
    matched = cv2.filter2D(thresh, cv2.CV_64F, kernel)
    matched = normalize(matched)

    # apply gaussian blur
    kernel = blur_kernel()
    blur = cv2.filter2D(matched, cv2.CV_64F, kernel)
    blur = normalize(blur)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(np.uint8(blur), cfg.SMOOTH_CUTOFF, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
# end function


#####################################################################################
# --------------------------- 2nd Level Functions --------------------------------- #
#####################################################################################


def normalize(img):
    """Rounds to nearest integer and clears out-of-boundary values.
    Intensity boundary is [0, 255].
    :param img: Image to apply normalize
    """
    tol = 355
    maxi = np.max(img)
    if maxi > tol:
        img = 255 * (img - (tol - 255)) / maxi
    # end if

    norm = np.round(img)
    norm[norm < 0] = 0
    norm[norm > 255] = 255

    return norm
# end function


def blur_kernel():
    """
    Build 2D Gaussian kernel 
    """

    # formula -- https://goo.gl/3AmmaE
    A = cfg.BLUR_CO
    m, n = cfg.BLUR_SIZE
    sx, sy = cfg.BLUR_SIGMA

    x0 = m / 2
    y0 = n / 2

    X = np.arange(m)
    Y = np.arange(n)

    X = np.square((X - x0) / sx)
    Y = np.square((Y - y0) / sy)

    Y, X = np.meshgrid(Y, X)
    kernel = A * np.exp(-(X + Y) / 2)

    return kernel
# end function


def intensity_calculate(row, col, gauss):
    """
    Calculate (mean, and standard deviation) values for Intensifying
    """
    m, n = cfg.BLOCK_COUNT
    h = row // m
    w = col // n

    x, y = np.ogrid[0:1:(1/h), 0:1:(1/w)]
    neg_x = np.float64(1 - x)
    neg_y = np.float64(1 - y)

    mean = np.zeros((row, col), dtype=np.float64)
    sdev = np.zeros((row, col), dtype=np.float64)

    # loop iterators
    win_x, win_y = np.ogrid[0:row:h, 0:col:w]
    win_x = win_x.flatten()
    win_y = win_y.flatten()

    # for all windows
    for i in win_x:
        for j in win_y:
            # local average of four corners
            i_a, d_a = mean_std(gauss, i, j, h, w)
            i_b, d_b = mean_std(gauss, i, j + w, h, w)
            i_c, d_c = mean_std(gauss, i + h, j, h, w)
            i_d, d_d = mean_std(gauss, i + h, j + w, h, w)

            # calculate local intensity
            upper_l = neg_y * i_a + y * i_b
            lower_l = neg_y * i_c + y * i_d
            mean[i:i + h, j:j + w] = np.dot(neg_x, upper_l) + np.dot(x, lower_l)

            # calculate local standard deviation
            upper_d = neg_y * d_a + y * d_b
            lower_d = neg_y * d_c + y * d_d
            sdev[i:i+h, j:j+w] = np.dot(neg_x, upper_d) + np.dot(x, lower_d)
        # end for j
    # end for i

    return mean, sdev
# end function


def mean_std(img, i, j, p, q):
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
    x1 = max(0, i - p // 2)
    y1 = max(0, j - q // 2)
    x2 = min(row, i + p // 2)
    y2 = min(col, j + q // 2)
    window = img[x1:x2, y1:y2]

    # calculate mean and std
    mean = np.mean(window)
    std = np.std(window / np.float64(255))
    return mean, std
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


def mixture_model():
    """
    Builds a gaussian kernel for mixture model
    """

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

    _, kernel = np.meshgrid(Y, H)
    return kernel
# end function

