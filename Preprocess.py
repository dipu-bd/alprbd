#!/usr/bin/python

import cv2
import math
import numpy as np

# module level variables ##########################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################
def preprocess(imgOriginal):

    imgScaled = scaleImage(imgOriginal)                  # scale image

    imgGrayscale = extractValue(imgScaled)               # make grayscale

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    height, width = imgGrayscale.shape
    imgBlurred = np.zeros((height, width, 1), np.uint8)  # fail safe copy of blur image
    imgBlurred = cv2.GaussianBlur(                       # blur image
        imgMaxContrastGrayscale,
        GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    imgThresh = cv2.adaptiveThreshold(                   # extract threshold
        imgBlurred, 255.0,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        ADAPTIVE_THRESH_BLOCK_SIZE,
        ADAPTIVE_THRESH_WEIGHT)

    return imgScaled, imgGrayscale, imgThresh
# end function

###################################################################################################
def scaleimage(imgOriginal):

    height, width = imgOriginal.shape       # original height and width

    ratio = 640.0 / width                   # new image ratio
    dim = (640, int(ratio * height))        # new dimension

    # perform the actual resizing of the image and show it
    imgResized = cv2.resize(imgOriginal, dim, interpolation=cv2.INTER_AREA)

    return imgResized
# end function

###################################################################################################
def extractValue(imgOriginal):
    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)             # fail safe copy
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
# end function

###################################################################################################
def maximizeContrast(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
# end function



