"""
Transforms an image using morphological operations
"""
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import config as cfg


def get_name(folder, index):
    return os.path.join(folder, '{:05d}.bmp'.format(index))
# end function


def bigframe(img):
    """
    Trims the image
    """
    r, c = img.shape
    out = np.zeros((3*r, 3*c), np.uint8)
    out[r:2*r, c:2*c] = img
    return out
# end function


def copy_image(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    cv2.imwrite(outfile, img)
# end function


def dilate(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(outfile, dilation)
# end function


def erode(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(outfile, erosion)
# end function


def median(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    median = cv2.medianBlur(img, 1)
    cv2.imwrite(outfile, median)
# end function


def affine1(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    
    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [20, 5], [6, 22]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, dst)
# end function


def affine2(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))

    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[6, 4], [10, 5], [6, 20]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, dst)
# end function


def affine3(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))

    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [10, 5], [4, 20]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, dst)
# end function


def tophat1(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, tophated)
# end function


def tophat2(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, tophated)
# end function


def tophat3(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, tophated)
# end function


def tophat4(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 12))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, tophated)
# end function


def trim(img):
    """
    Trims the image
    """
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 1)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 1)
    # crop
    return img[x1:x2, y1:y2]
# end function


def normalize_image(file, scale):
    image = cv2.imread(file, 0)
    image = trim(image)
    image[image < 100] = 0
    image[image > 0] = 255
    image = cv2.resize(image, scale)
    cv2.imwrite(file, image)
# end function


def transform(file, index):
    """
    Uses various transformation on image
    """

    start = index
    folder = os.path.dirname(file)

    scale = (28, 28)
    if os.path.dirname(folder).startswith(cfg.CITY_PATH):
        scale = (28, 4*28)
    # end if
    normalize_image(file, scale)

    # units
    functions = [
        median,
        dilate,

        affine1,
        affine2,
        affine3,
        
        affine1,
        affine2,
        affine3,
        
        tophat1,
        tophat2,
        tophat3,
        tophat4,
        
        copy_image,
        copy_image,
        copy_image,
    ]

    for fT1 in functions:
        fn1 = fT1.__name__[:-1]
        # original units 
        index += 1
        out = get_name(folder, index)
        fT1(file, out)
        normalize_image(out, scale)
        # mixture units
        for fT2 in functions:
            fn2 = fT1.__name__[:-1]
            if fn1 == 'tophat' and fn1 == fn2: 
                continue
            # apply second transformation
            index += 1
            out2 = get_name(folder, index)
            fT2(out, out2)
            normalize_image(out2, scale)
        #end for
    # end for
        
    return index
# end function
