"""
Pre-process image
"""
import cv2
from alprbd import config as cfg


def process(image):
    """
    Process img in order to make alpr-task easier
    :param img: Image object
    :return: Image object after processing
    """
    image.scaled = rescale(image.original)
    image.gray = convert_gray(image.scaled)
    image.enhanced = enhance(image.gray)
    return image


def convert_gray(img):
    """
    converts image to gray-scale
    :param img: original image
    :return: grayscale image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def rescale(img):
    """
    resize image to a predefined dimension
    :param img: original image
    :return: rescaled image
    """
    return cv2.resize(img, cfg.SCALE_DIM, interpolation=cv2.INTER_AREA)


def enhance(img):
    """
    enhance image contrast
    :param img: original image
    :return: enhanced image
    """
    # http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    return clahe.apply(img)
