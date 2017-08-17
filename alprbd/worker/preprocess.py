"""
Pre-process image
"""
import cv2
import numpy as np
import alprbd.config as cfg
from ..models import Region

# ---------- Clip Limited Adaptive Histogram Enhancement Function -----------
# http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
CLAHE = cv2.createCLAHE(clipLimit=2.3, tileGridSize=(30, 60))       # for image
ROI_CLAHE = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))     # for ROIs


def process(frame):
    """
    Process img in order to make alpr-task easier
    :param frame: Image object
    :return: Image object after processing
    """
    frame.scaled = rescale(frame.original, cfg.SCALE_DIM)
    frame.gray = to_gray(frame.scaled)
    frame.enhanced = CLAHE.apply(frame.gray)
    return frame
# end function

def to_gray(img):
    """
    Returns a grayscale image with predefined formula
    """
    b, g, r = cv2.split(img)
    img = np.uint8(0.299 * r + 0.587 * g + 0.114 * b)
    return img
# end def

def auto_crop(img):
    """
    Crop image to keep the foreground only.
    :param img: image to crop
    :return: cropped image
    """
    # check image
    if img is None:
        return None
    # end if
    row, col = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(row, np.max(nzx))
    y1 = max(0, np.min(nzy))
    y2 = min(col, np.max(nzy))
    # crop
    return img[x1:x2, y1:y2]
# end function


def rescale(img, dst_size):
    """
    Resize image to keeping aspect ratio
    :param img: original image
    :param dst_size: destination size
    :return: rescaled image
    """
    height, width = img.shape[:2]
    new_width, new_height = dst_size[:2]
    if height < width:
        new_width = (width * new_height) // height
    else:
        new_height = (height * new_width) // width
    # end if
    return cv2.resize(img, (new_width, new_height))
# end function


def get_binaries(img):
    """
    gets two binary images of given image
    :param img: image to convert
    :return: array of [binary, inverse binary] image
    """
    # process image
    img = rescale(img, cfg.PLATE_DIM)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = ROI_CLAHE.apply(img)

    _, binary1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)

    return [binary1, binary2]
# end function


def box2region(box, region):
    """
    convert one region to another
    :param box: current region
    :param region: destination region
    :return: converted region
    """
    [[x1, x2, y1, y2], [row, col]] = box
    height, width = region.height, region.width
    w = (y2 - y1) * col // width
    h = (x2 - x1) * row // height
    x = x1 * row // height + region.x
    y = y1 * col // width + region.y
    return Region(region.parent, x, y, h, w)
# end function
