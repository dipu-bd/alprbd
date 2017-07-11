"""
Pre-process image
"""
import cv2
from ..helper import config as cfg


def process(image):
    convert_gray(image)
    rescale(image)
    pass


def convert_gray(image):
    b, g, r = cv2.split(image.image)
    ratio = cfg.GRAY_RATIO
    gray = r * ratio.R + g * ratio.G + b * ratio.B
    image.gray = gray
    pass


def rescale(image):
    image.scaled = cv2.resize(image.image,
                              cfg.SCALE_DIM,
                              interpolation=cv2.INTER_AREA)
    pass


