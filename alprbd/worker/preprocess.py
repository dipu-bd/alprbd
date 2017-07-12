"""
Pre-process image
"""
import cv2
import alprbd.config as cfg
from ..helper.image_util import rescale


def process(frame):
    """
    Process img in order to make alpr-task easier
    :param frame: Image object
    :return: Image object after processing
    """
    frame.scaled = rescale(frame.original, cfg.SCALE_DIM)
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


def enhance(img):
    """
    enhance image contrast
    :param img: original image
    :return: enhanced image
    """
    # http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(20, 40))
    return clahe.apply(img)
# end function