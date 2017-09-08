"""
Transforms an image using morphological operations
"""
# -*- coding: utf-8 -*-

import os
from shutil import copyfile
import cv2
import numpy as np
import config as cfg


def transform(file, index):
    """
    Uses various transformation on image
    """
    normalize_image(file)

    # transformers
    transformers = [
        median,
        dilate,
    ]
    transformers.extend([
        affine1,
        affine2,
        affine3
    ] * 2)
    transformers.extend([
        copyfile
    ] * 3)

    # special transformers
    specials = [
        noisy
    ]
    specials.extend([
        copyfile
    ] * 20)

    # apply transformers
    folder = os.path.dirname(file)
    for function1 in transformers:
        index += 1
        out = get_name(folder, index)
        function1(file, out)
        normalize_image(out)
        for function2 in transformers:
            index += 1
            out2 = get_name(folder, index)
            function2(out, out2)
            normalize_image(out2)
        # end for
    # end for

    return index
# end function

def get_name(folder, index):
    """returns the name of new file"""
    return os.path.join(folder, '{:05d}.bmp'.format(index))
# end function


#-------------------------------------------------------------------#
#                     ALL TRANSFORMATIONS                           #
#-------------------------------------------------------------------#

def dilate(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(outfile, dilation)
# end function


def erode(infile, outfile):
    img = cv2.imread(infile, 0)
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


def noisy(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = np.random.rand(*img.shape)
    noisy = img * kernel
    cv2.imwrite(outfile, noisy)
# end function


#-------------------------------------------------------------------#
#                           OTHER METHODS                           #
#-------------------------------------------------------------------#

def bigframe(img):
    """
    Trims the image
    """
    r, c = img.shape
    out = np.zeros((3*r, 3*c), np.uint8)
    out[r:2*r, c:2*c] = img
    return out
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

def normalize_image(file):
    img = cv2.imread(file, 0)
    img = trim(img)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    img = cv2.resize(img, (28, 28))
    cv2.imwrite(file, img)
# end function
