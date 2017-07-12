"""
Pre-process image
"""
import cv2
from alprbd import config as cfg


def process(frame):
    """
    Process img in order to make alpr-task easier
    :param frame: Image object
    :return: Image object after processing
    """
    frame.scaled = rescale(frame.original)
    frame.gray = convert_gray(frame.scaled)
    frame.enhanced = enhance(frame.gray)
    return frame
# end function


def convert_gray(img):
    """
    converts image to gray-scale
    :param img: original image
    :return: grayscale image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# end function


def rescale(img):
    """
    resize image to a predefined dimension
    :param img: original image
    :return: rescaled image
    """
    h, w = img.shape
    d_w, d_h = cfg.SCALE_DIM
    if h < w:
        w = w * d_h / h
        h = d_h
    else:
        h = h * d_w / w
        w = d_w
    # end if
    return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
# end function


def enhance(img):
    """
    enhance image contrast
    :param img: original image
    :return: enhanced image
    """
    # http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    return clahe.apply(img)
# end function