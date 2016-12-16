
import os
import sys
import cv2

import Preprocess as pp

###################################################################################################
def main(img_file):
    """Start point of the application.

    Keyword arguments:
    img_file -- the image file to use for ALPR
    """

    img_original = cv2.imread(img_file)                     # open image

    if img_original is None:                                # if image was not read successfully
        print "\nERROR: count not read image file \n"       # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    scaled, grayscale, thresh = pp.preprocess(img_original)

    cv2.imshow("Scaled Image", scaled)
    cv2.waitKey(0)

    cv2.imshow("Grayscale Image", grayscale)
    cv2.waitKey(0)

    cv2.imshow("Threshold Applied", thresh)
    cv2.waitKey(0)

# end main

###################################################################################################

if __name__ == "__main__":
    main(sys.argv[1])





