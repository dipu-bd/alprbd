# -*- coding: utf-8 -*-

import cv2
import numpy as np
from os import path
import config as cfg


def extract(img):
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
        roi = img[x1:x2, y1:y2]
        edges = detect_edges(roi)
		regions = check_contours(roi, edges)

		for bound in regions: 
			plate = get_plate(bound)
			binary = get_binary(plate)
			clean = denoise(binary)
			if clean is not None:
				plates.append(clean)
			# end if 
		# end for
    # end for

    return plates
# end function


#####################################################################################
# --------------------------- 1st Level Functions --------------------------------- #
#####################################################################################

def grayscale(img):
    # grayscale 
    b, g, r = cv2.split(scaled)
    gray = cfg.GRAY_RATIO[0] * r + cfg.GRAY_RATIO[1] * g + cfg.GRAY_RATIO[2] * b    
    return np.uint8(gray)
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
    ret = f(sdev) * (img - mean) + mean

    # normalize and return
    ret[ret < 0] = 0
    ret[ret > 255] = 255
    return np.uint8(ret)
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

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(blur, cfg.SMOOTH_CUTOFF, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
# end function


#####################################################################################


def check_contours(img, canny):
    """
    Locate plate regions
    :param img: scaled image 
    :param canny: image after canny edge detection algorithm is applied
    """
    height, width = img.shape
    img_area = height * width

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    regions = []
    for cnt in contours:
        # get bounding box
        y, x, col, row = cv2.boundingRect(cnt)

        # check height and width
        if row >= col or row < cfg.MIN_HEIGHT or col < cfg.MIN_WIDTH:
            continue
        # end if

        # check area
        area = row * col
        if area / img_area < cfg.MIN_AREA:
            continue
        # end if

        # check aspect ratio
        aspect = row / col
        if aspect < cfg.MIN_ASPECT or aspect > cfg.MAX_ASPECT:
            continue
        # end if

        # minimum area box
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)

        # check rotation
        angle = abs(rect[2])
        if cfg.MAX_ANGLE < angle < 90 - cfg.MAX_ANGLE:
            continue
        # end if

        # get region data
        region = [[x, x+row, y, y+col], box]
        regions.append(region)
    # end for

    return regions
# end function


def detect_edges(plate):
    # grayscale 
    gray = grayscale(plate)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(gray, cfg.SMOOTH_CUTOFF, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Canny edge detection
    canny = cv2.Canny(thresh, 100, 200, L2gradient=True)

    return canny
# end function


def get_plate(img, region):
    """
    Extract plate image and fix rotation
    :param img: original plate image
    :param region: region information
    """
    # extract plate
    box = region[1]
    x1, x2, y1, y2 = region[0]
    plate = img[x1:x2, y1:y2]

    # calculate rotation angle
    angle = abs(box[2])
    if angle < 45:
        angle = -angle
    else:
        angle = 90 - angle
    # end if

    # rotate plate
    cols = y2 - y1
    rows = x2 - x1
    rot_mat = cv2.getRotationMatrix2D(box[1], angle, 1)
    out = cv2.warpAffine(plate, rot_mat, (cols, rows))

    # resize plate
    scaled = cv2.resize(out, cfg.PLATE_DIM)

    return scaled
# end function


#####################################################################################

def get_binary(img):
    """
    Converts to black and white / binary image   
    :param img: plate image 
    """
    # normal binary threshold
    bnw1 = cv2.threshold(np.uint8(img), cfg.BNW_THRESH, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # inverse binary threshold
    bnw2 = cv2.threshold(np.uint8(img), cfg.BNW_THRESH, 255,
                         cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # calculate ratio of non-zero pixels
    row, col = img.shape
    area = row * col
    ratio1 = cv2.countNonZero(bnw1) / area
    ratio2 = cv2.countNonZero(bnw2) / area

    # return image with lower ratio
    bnw = bnw2
    if ratio1 < ratio2:
        bnw = bnw1
    # end if

    # normalize
    bnw[bnw <= 127] = 0
    bnw[bnw > 127] = 255
    return bnw
# end function


def denoise(img):
    """
    Remove noise.
    :param img: plate image 
    """
    row, col = img.shape
    img[img < 128] = 0
    img[img > 0] = 255

    # de-noise using contours
    contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    for cnt in contours:
        y, x, n, m = cv2.boundingRect(cnt)
        if 35 < m < row - 25 and 35 < n < col - 25:
            continue
        # end if

        cv2.fillConvexPoly(img, cnt, 0)
        # rect = cv2.minAreaRect(cnt)
        # box = np.int32(cv2.boxPoints(rect))
        # cv2.fillConvexPoly(img, box, 0)
    # end for

    # check mean white pixels
    if np.mean(img) < 8:
        return None
    # end if

    return img
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


