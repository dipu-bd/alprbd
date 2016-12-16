
import os
import sys
import cv2

import Preprocess as pp

###################################################################################################
def main(imgFile):
    """Start point of the application.

    Keyword arguments:
    imgFile -- the image file to use for ALPR
    """

    imgOriginal = cv2.imread(imgFile)                     # open image

    if imgOriginal is None:                                # if image was not read successfully
        print "\nERROR: count not read image file \n"       # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    imgScaled, imgGrayscale, imgThresh = pp.preprocess(imgOriginal)

    #TEST(imgGrayscale)  

    cv2.imshow("Scaled Image", imgScaled)
    cv2.waitKey(0)

    cv2.imshow("Grayscale Image", imgGrayscale)
    cv2.waitKey(0)

    cv2.imshow("Threshold Applied", imgThresh)
    cv2.waitKey(0)

# end main

###################################################################################################

def TEST(gray):
 
    blurred = gray
   # blurred = cv2.GaussianBlur(pp.maximizeContrast(gray), (3, 3), 0)

    values = [[5,7], [9,7], [19,7], [11,9], [29,9], [19,9]]
    for v in values:
        thresh = cv2.adaptiveThreshold(                   # extract threshold
            blurred, 255.0,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, v[0], v[1])
        outFile = "/home/dipu/Desktop/out/" + str(v[0]) + "." + str(v[1]) + ".jpg"
        print outFile
        cv2.imwrite(outFile, thresh)

# end TEST

if __name__ == "__main__":
    main(sys.argv[1])





