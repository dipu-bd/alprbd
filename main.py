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

        cv2.imwrite(outFile + "/1 original.jpg", res[0]);
        cv2.imwrite(outFile + "/2 grayscale.jpg", res[1]);
        cv2.imwrite(outFile + "/3 blurred.jpg", res[2]);
        cv2.imwrite(outFile + "/4 threshold.jpg", res[3]);
        cv2.imwrite(outFile + "/5 scaled.jpg", res[4]);
        cv2.imwrite(outFile + "/6 detected edges.jpg", res[5]);
    #end for

    print "\nDONE\n"
# end process files

###############################################################################

def processImage(img):

    # make grayscale
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)
    gray = val

    # apply blur
    blur = cv2.medianBlur(gray, 5)

    # apply threshold value
    thres = cv2.adaptiveThreshold(blur, 255,\
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                  cv2.THRESH_BINARY, 51, 7)

    # scale image
    scaled = scaleImage(img, 1024, 768)

    # canny edge detection
    edges = cv2.Canny(blur, 100,200)

    return [img, gray, blur, thres, scaled, edges]

# end processImage

def scaleImage(img, newWidth, newHeight):

    height, width = img.shape[:2]

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
