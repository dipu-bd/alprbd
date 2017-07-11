"""
Pre-process image
"""
import cv2
from alprbd import config as cfg


def process(img):
    """
    Process img in order to make alpr-task easier
    :param img: Image object
    :return: Image object after processing
    """
    img.scaled = rescale(img.original)
    img.gray = convert_gray(img.scaled)
    return img


def convert_gray(image):
    """converts image to gray-scale"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def rescale(image):
    """resize image to a predefined dimension"""
    return cv2.resize(image, cfg.SCALE_DIM, interpolation=cv2.INTER_AREA)


