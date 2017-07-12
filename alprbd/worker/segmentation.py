"""
Contains methods used to segment the license plate
"""
import cv2
import numpy as np
import alprbd.config as cfg


def segment(frame):
    """
    Segments the license plate characters
    :param frame: Image frame to process
    :return: Processed frame
    """
    plates = []
    for plate in frame.plates:
        segs = get_segments(plate.image)
        if len(segs) >= 8:
            plate.segments = segs
            plates.append(plate)
        # end if
    # end for
    frame.plates = plates
    return frame
# end function


def get_segments(img):
    """
    Calculate the horizontal projections.
    :param img: img to segment
    """
    # calculate horizontal projections
    hors = horizontal(img)

    # calculate vertical projections
    vers = []
    for x in hors:
        vers.extend(vertical(x))
    # end for

    return vers
# end function


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

    plate = trim_image(plate)
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

    plate = trim_image(plate)
    if isvalid(plate):
        ver.append(plate)
    # end if

    return ver
# end if


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


def trim_image(img):
    """Keep only important part"""
    # check image
    if img is None:
        return None
    # end if
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 2)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 2)
    # crop
    return img[x1:x2, y1:y2]
# end function
