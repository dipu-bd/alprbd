"""
Utility functions to transform image
"""
import cv2
import numpy as np


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
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx))
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy))
    # crop
    return img[x1:x2, y1:y2]
# end function


def auto_rotate(img):
    """
    Apply affine transformation to fix image angle
    :param img: image to rotate
    :return: rotated image
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is None:
        return img

    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img
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
