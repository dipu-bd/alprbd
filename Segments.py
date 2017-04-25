# -*- coding: utf-8 -*-

import cv2
import numpy as np 

#####################################################################################

def do(img):
    """
    Calculate the horizontal projections.
    :param img: plate image 
    """
    # calculate horizontal projections
    hors = horizontal(img)

    # calculate vertical projections
    vers = []
    for x in hors:
        vers.extend(vertical(x))
    # end for

    # final trimming
    segments = []
    for x in vers:
        segments.extend(horizontal(x))
    # end for

    return segments
# end function

#####################################################################################

def horizontal(img):
    """
    Calculate the horizontal segments.
    :param img: plate image 
    """
    hor = []
    plate = None
    row_sum = np.mean(img, axis=1)
    for r, v in enumerate(row_sum):
        if v > 1:
            if plate is None:
                plate = img[r:r+1, :]
            else:
                plate = np.vstack((plate, img[r:r+1, :]))
            # end if
        else:
            if isvalid(plate):
                hor.append(plate)
                plate = None
            # end if
        # end if
    # end for
    if isvalid(plate):
        hor.append(plate)
    # end if

    return hor
# end if


def vertical(img):
    """
    Calculate the horizontal segments.
    :param img: plate image 
    """
    ver = []
    plate = None
    col_sum = np.mean(img, axis=0)
    for c, v in enumerate(col_sum):
        if v > 2:
            if plate is None:
                plate = img[:, c:c+1]
            else:
                plate = np.hstack((plate, img[:, c:c+1]))
            # end if
        else:
            if isvalid(plate):
                ver.append(plate)
                plate = None
            # end if
        # end if
    # end for
    if isvalid(plate):
        ver.append(plate)
    # end if

    return ver
# end if

#####################################################################################

def isvalid(plate):
    """
    Checks whether the plate is valid
    :param plate: 
    :return: 
    """
    if plate is None:
        return False
    # end if

    row, col = plate.shape
    if row < 12 or col < 12:
        return False
    # end if

    if np.mean(plate) < 5:
        return False
    # end if

    return True
# end if


