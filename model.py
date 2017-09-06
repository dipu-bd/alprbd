""" Unlicensed """
from collections import OrderedDict
import cv2
import numpy as np
from node import Node, Var

IMAGE = 'jpg'
ARRAY = 'txt'

def Model():
    """Get an operational model"""
    m = OrderedDict()
    m['_file'] = Var(None)
    m['open'] = Node(cv2.imread, m['_file'], ext=IMAGE)
    m['image_dim'] = Node(calculate_resize_amount, m['open'])
    m['resize'] = Node(cv2.resize, m['open'], m['image_dim'], ext=IMAGE)
    m['gray'] = Node(to_gray, m['resize'], ext=IMAGE)
    m['clahe'] = Node(apply_clahe, m['gray'], Var(30, 60), Var(2.3), ext=IMAGE)
    m['sobel'] = Node(cv2.Sobel, m['clahe'], Var(-1), Var(1), Var(0), ksize=3, ext=IMAGE)
    m['thresh_sobel'] = Node(cv2.threshold, m['sobel'], Var(127), Var(255), Var(cv2.THRESH_TOZERO), ext=IMAGE)
    m['match'] = Node(match_filter, ext=IMAGE)
    m['blur'] = 
    m['thresh_blur']
    m['contours']



    return m
# end def


def calculate_resize_amount(img):
    row, col = img.shape[:2]
    return (640, 640 * row // col)
# end def

def to_gray(img):
    b, g, r = cv2.split(img)
    return np.uint8(0.299 * r + 0.587 * g + 0.114 * b)
# end def

def apply_clahe(img, kernel=(8, 8), clip=1.0):
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=kernel)
    return clahe.apply(img)
# end def
