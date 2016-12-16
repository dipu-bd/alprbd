#!/usr/bin/python

import os
import cv2
import Preprocess

###################################################################################################
def main(imgFile):

    imgOriginal  = cv2.imread(imgFile)                        # open image

    if imgOriginal is None:                                 # if image was not read successfully
        print "\nerror: count not read image file \n\n"     # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    cv2.imshow("imgOriginal", imgOriginal)                  # show scene image

    imgGrayscale, imgThresh = preprocess(imgOriginal)                  # calls pre-process routines

    cv2.imgshow("imgGrayscale", imgGrayscale)
    cv2.imgshow("imgThresh", imgThresh)

    cv2.waitKey(0)					# hold windows open until user presses a key
    return
# end main

###################################################################################################

if __name__ == "__main__":
    main(sys.argv[2])





