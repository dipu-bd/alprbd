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
    height = img.shape[0]
    width = img.shape[1]
    dst_width, dst_height = cfg.SCALE_DIM
    if height < width:
        width = (width * dst_height) // height
        height = dst_height
    else:
        height = (height * dst_width) // width
        width = dst_width
    # end if
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
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