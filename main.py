# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from shutil import rmtree

###############################################################################

def main():
    inPath = "test"
    outPath = "out"

    if not os.path.exists(inPath):
        print 'error: no input folder'
        return
    #end if

    if os.path.exists(outPath):
        rmtree(os.path.abspath(outPath))
    #end if


    # get all image files from input folder
    exts = ['jpg', 'png', 'bmp']
    files = os.listdir(inPath)
    files = filter(lambda name: any(st in name.lower() for st in exts), files)
    files.sort()

    # process all image files
    for f in files:
        # convert to absolute url
        imgFile = inPath + "/" + f
        imgFile = os.path.abspath(imgFile)
        print imgFile

        # open original image
        img = cv2.imread(imgFile)

        # pre-process
        res = processImage(img)

        outFile = outPath + "/" + f
        os.makedirs(outFile)

        for name, img in res:
            cv2.imwrite(outFile + "/" + name + ".jpg", img)
        #end for

    #end for

    print "\n--------- DONE ---------\n"

# end process files

###############################################################################

def processImage(img):

    # make grayscale
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)
    gray = val

    # apply blur
    blur = cv2.medianBlur(gray, 3)

    # scale image
    scaled = scaleImage(blur, 1024, 768)

    # working copy of image
    work = blur

    # canny edge detection
    edges = cv2.Canny(work, 100,200)

    # laplacian algo
    laplacian = cv2.Laplacian(work, cv2.CV_64F)

    # sobel operators
    sobelx = cv2.Sobel(work, cv2.CV_64F, 1,0,ksize=5)
    sobely = cv2.Sobel(work, cv2.CV_64F, 0,1,ksize=5)


    # apply threshold value on edges
    thres = cv2.adaptiveThreshold(work, 255,\
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                  cv2.THRESH_BINARY, 51, 7)


    return [\
            ["1 original", img],\
            ["2 grayscale", gray],\
            ["3 blur", blur],\
            ["4 scaled", scaled],\
            ["5 threshold", thres],\
            ["6 edges", edges],\
            ["7 laplacian", laplacian],\
            ["8 sobel-x", sobelx],\
            ["9 sobel-y", sobely],\
        ]

# end processImage

def scaleImage(img, newWidth, newHeight):

    height, width = img.shape[:2]

    newWidth = min(width, newWidth)
    newHeight = min(height, newHeight)

    if height < width:
        newHeight =  height * newWidth / width
    else:
        newWidth = width * newHeight / height
    #end if

    dim = (int(newWidth), int(newHeight))

    res = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
    return res

# end scaleImage

###############################################################################
if __name__ == "__main__":
    main()
