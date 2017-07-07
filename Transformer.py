"""
Transforms an image using morphological operations
"""
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


def get_name(folder, index):
    return os.path.join(folder, '{:04d}.bmp'.format(index))
# end function


def normalize_image(image):
    #image[image > 0] = 255
    return image
# end function


def dilate(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = np.ones((1, 2), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(dilation))
# end function


def erode(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = np.ones((2, 1), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(erosion))
# end function


def tophat1(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat2(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat3(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat4(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (8, 8))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def median(infile, outfile):
    img = cv2.imread(infile, 0)
    median = cv2.medianBlur(img, 5)
    cv2.imwrite(outfile, normalize_image(median))
# end function


def affine1(infile, outfile):
    img = cv2.imread(infile, 0)
    rows, cols = img.shape

    pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
    pts2 = np.float32([[3, 6], [20, 5], [7, 22]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def affine2(infile, outfile):
    img = cv2.imread(infile, 0)
    rows, cols = img.shape

    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[6, 4], [10, 5], [7, 20]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def transform(file, index):
    """
    Uses various transformation on image
    """

    folder = os.path.dirname(file)

    # units
    functions = [
        median,
        affine1,
        affine2,
        dilate,
        erode,
        tophat1,
        tophat2,
        tophat3,
        tophat4,
    ] 

    for fT in functions:
        # original units 
        index += 1
        out = get_name(folder, index)
        fT(file, out)        
        # mixture units
        for fT2 in functions:
            index += 1
            out2 = get_name(folder, index)            
            fT2(out, out2)
        #end for
    # end for

    return index
# end function