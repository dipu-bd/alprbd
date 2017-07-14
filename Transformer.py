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
    x2 = min(rows, np.max(nzx) + 1)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 1)
    # crop
    return img[x1:x2, y1:y2]
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


def normalize_image(image):
    image = trim(image)
    image[image < 100] = 0
    image[image > 0] = 255
    return image
# end function


def copy_image(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    cv2.imwrite(outfile, normalize_image(img))
# end function


def dilate(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(dilation))
# end function


def erode(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(outfile, normalize_image(erosion))
# end function


def median(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    median = cv2.medianBlur(img, 1)
    cv2.imwrite(outfile, normalize_image(median))
# end function


def affine1(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    
    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [20, 5], [6, 22]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def affine2(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))

    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[6, 4], [10, 5], [6, 20]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def affine3(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))

    rows, cols = img.shape
    pts1 = np.float32([[5, 5], [10, 5], [5, 20]])
    pts2 = np.float32([[4, 6], [10, 5], [4, 20]])
    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(outfile, normalize_image(dst))
# end function


def tophat1(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat2(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 6))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat3(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def tophat4(infile, outfile):
    img = bigframe(cv2.imread(infile, 0))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 12))
    tophated = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite(outfile, normalize_image(tophated))
# end function


def transform(file, index):
    """
    Uses various transformation on image
    """

    folder = os.path.dirname(file)

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
        #tophat2,
        #tophat3,
        tophat4,
        
        copy_image,
        copy_image,
        copy_image,
    ]

    for fT in functions:
        # original units 
        index += 1
        out = get_name(folder, index)
        fT(file, out)
        # mixture units
        for fT2 in functions:
            if(fT.__name__ == fT2.__name__):
                continue
            # end if
            index += 1
            out2 = get_name(folder, index)            
            fT2(out, out2)
        #end for
    # end for

    return index
# end function
