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


def trim(img):
    """
    Trims the image
    """
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 2)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 2)
    # crop
    cropped = img[x1:x2, y1:y2]
    # resize
    resized = cv2.resize(cropped, cfg.IMAGE_DIM)    

    return resized
# end function


def normalize_image(image):
    image = trim(image)
    #image[image < 128] = 0
    #image[image > 0] = 255
    return image
# end function


def copy_image(infile, outfile):
    img = cv2.imread(infile, 0)
    cv2.imwrite(outfile, normalize_image(img))
# end function


def dilate(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(dilation))
# end function


def erode(infile, outfile):
    img = cv2.imread(infile, 0)
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(erosion))
# end function


def median(infile, outfile):
    img = cv2.imread(infile, 0)
    median = cv2.medianBlur(img, 1)
    cv2.imwrite(outfile, normalize_image(median))
# end function


def affine1(infile, outfile):
    img = cv2.imread(infile, 0)
    rows, cols = img.shape

    pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [20, 5], [6, 22]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def affine2(infile, outfile):
    img = cv2.imread(infile, 0)
    rows, cols = img.shape

    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[6, 4], [10, 5], [6, 20]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def affine3(infile, outfile):
    img = cv2.imread(infile, 0)
    rows, cols = img.shape

    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [10, 5], [4, 20]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
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
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 12))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def transform(file, index):
    """
    Uses various transformation on image
    """

    folder = os.path.dirname(file)

    copy_image(file, file)

    # units
    functions = [
        copy_image,
        median,
        copy_image,
        affine1,
        copy_image,
        affine2,
        copy_image,
        affine3,
        copy_image,
        dilate,
        copy_image,
        erode,
        copy_image,
        tophat1,
        copy_image,
        #tophat2,
        copy_image,
        #tophat3,
        copy_image,
        tophat4,
        copy_image,
    ]

    for fT in functions:
        # original units 
        index += 1
        out = get_name(folder, index)
        fT(file, out)
        #continue 
        # mixture units
        for fT2 in functions:
            index += 1
            out2 = get_name(folder, index)            
            fT2(out, out2)
        #end for
    # end for

    return index
# end function
