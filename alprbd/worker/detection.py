"""
Declaration of methods used for plate detection.
"""
import cv2
import numpy as np
from ..models import Region


def detect_roi(frame):
    """
    Detects all regions of interest
    :param frame: Image object
    :return: Image object with ROIs
    """
    # apply matching
    matched = apply_matching(frame.enhanced)
    scaled_height, scaled_width = matched.shape

    # locate all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(matched, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract clean plates
    frame.roi = []
    for cnt in contours:
        # get bounding box
        y, x, c, r = cv2.boundingRect(cnt)

        # check image size
        if not (r < c and 20 < r < 150 and 60 < c < 350):
            continue
        # end if

        # translate points
        x = (x * frame.height) // scaled_height
        y = (y * frame.width) // scaled_width
        r = (r * frame.height) // scaled_height
        c = (c * frame.width) // scaled_width

        # original ROI
        frame.roi.append(Region(frame, x, y, r, c))
    # end for

    return frame
# end function


def apply_matching(img):
    """
    Apply the special match filter highlight high density regions
    :param img:
    :return:
    """
    # vertical Sobel operator -- https://goo.gl/3fQnc9
    sobel = cv2.Sobel(img, -1, 1, 0, ksize=3)

    # thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(sobel, 100, 255, cv2.THRESH_TOZERO)

    # apply matched filter
    kernel = match_filter()
    matched = cv2.filter2D(thresh, -1, kernel)

    # apply gaussian blur
    blur = cv2.GaussianBlur(matched, (15, 15), 0)

    # Otsu's thresholding -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_OTSU)
    return thresh
# end function


def match_filter():
    """
    Builds a gaussian match filter
    """
    # formula -- @article(joarder2012bangla)
    m, n = 10, 20           # window size
    A, B = 0.003, -0.001    # intensity
    sa, sb = 15.0, 10.0     # spreading

    a = 3  # 0 to a
    b = 5  # b to m

    x1 = m // 6
    x2 = a + m // 6
    x3 = b + m // 6

    X = np.arange(m)
    Y = np.arange(n)

    X1 = X[:a]
    X2 = X[a:b]
    X3 = X[b:]

    X1 = np.square((X1 - x1) / sa)
    X2 = np.square((X2 - x2) / 1.0)
    X3 = np.square((X3 - x3) / sb)

    H1 = A * np.exp(-X1 / 0.2)
    H2 = B * np.exp(-X2 / 2.0)
    H3 = A * np.exp(-X3 / 0.2)
    H = np.hstack((H1, H2, H3))

    _, kernel = np.meshgrid(Y, H)
    return kernel
# end function
