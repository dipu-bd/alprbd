"""
Declaration of methods used of plate extraction.
"""
import cv2
import numpy as np
from alprbd import config as cfg
from ..models import Plate, Region
from .preprocess import get_binaries, auto_crop


def extract(frame):
    """
    Pick out all valid regions of interest
    :param frame: Image frame
    :return: Image frame after processing
    """
    frame.plates = []
    for region in frame.roi:
        blur = cv2.bilateralFilter(region.image, 7, 25, 50)
        for binary in get_binaries(blur):
            # clean and add img
            clean = denoise(binary)
            if clean is not None:
                frame.plates.append(Plate(region, clean))
            # end if

            # check contours
            for bound in check_contours(binary):
                extracted = get_plate(binary, bound)
                clean = denoise(extracted)
                if clean is not None:
                    x1, x2, y1, y2 = bound[0]
                    reg = Region(frame, x1, y1, x2 - x1, y2 - y1)
                    frame.plates.append(Plate(reg, clean))
                # end if
            # end for
        # end for
    return frame
# end function


def check_contours(img):
    """
    Locate plate regions
    :param img: ROI image
    """
    height, width = img.shape
    img_area = height * width

    # Otsu threshold -- https://goo.gl/6n5Kgn
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)

    # Canny edge detection
    canny = cv2.Canny(thresh, 100, 200, L2gradient=True)

    # map all contours -- http://stackoverflow.com/a/41322331/1583052
    contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    # extract plate like regions
    regions = []
    for cnt in contours:
        # get bounding box
        y, x, col, row = cv2.boundingRect(cnt)

        # check height and width
        if row >= col or row < cfg.MIN_HEIGHT or col < cfg.MIN_WIDTH:
            continue
        # end if

        # check area
        area = row * col
        if area / img_area < cfg.MIN_AREA:
            continue
        # end if

        # check aspect ratio
        aspect = row / col
        if aspect < cfg.MIN_ASPECT or aspect > cfg.MAX_ASPECT:
            continue
        # end if

        # minimum area box
        rect = cv2.minAreaRect(cnt)

        # check rotation
        angle = abs(rect[2])
        if cfg.MAX_ANGLE < angle < 90 - cfg.MAX_ANGLE:
            continue
        # end if

        # get region data
        region = [[x, x + row, y, y + col], rect]
        regions.append(region)
    # end for

    return regions
# end function


def get_plate(img, region):
    """
    Extract plate image and fix rotation
    :param img: original plate image
    :param region: region information
    """
    # extract plate
    box = region[1]
    x1, x2, y1, y2 = region[0]
    plate = img[x1:x2, y1:y2]

    # calculate rotation angle
    angle = abs(box[2])
    if angle < 45:
        angle = -angle
    else:
        angle = 90 - angle
    # end if

    # rotate plate
    cols = y2 - y1
    rows = x2 - x1
    rot_mat = cv2.getRotationMatrix2D(box[1], angle, 1)
    out = cv2.warpAffine(plate, rot_mat, (cols, rows))

    # resize plate
    scaled = cv2.resize(out, cfg.PLATE_DIM)
    return scaled
# end function


def get_binary(img):
    """
    Converts to black and white / binary image
    :param img: plate image
    """
    # normal binary threshold
    bnw1 = cv2.threshold(np.uint8(img), 50, 255, cv2.THRESH_OTSU)[1]

    # inverse binary threshold
    bnw2 = cv2.threshold(np.uint8(img), 50, 255, cv2.THRESH_OTSU)[1]

    # calculate ratio of non-zero pixels
    row, col = img.shape
    area = row * col
    ratio1 = cv2.countNonZero(bnw1) / area
    ratio2 = cv2.countNonZero(bnw2) / area

    # return image with lower ratio
    if ratio1 < ratio2:
        return bnw1
    else:
        return bnw2
    # end if
# end function


def denoise(img):
    """
    Remove noise.
    :param img: plate image
    """
    row, col = img.shape

    # remove borders
    upper = img[0:1, :]
    lower = img[row - 1:row, :]
    left = img[:, 0:1]
    right = img[:, col - 1:col]

    apply_flood_fill(img, upper)
    apply_flood_fill(img, lower, tx=row - 1)
    apply_flood_fill(img, left)
    apply_flood_fill(img, right, ty=col - 1)

    # de-noise using contours
    for i in range(1):
        for cnt in cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]:
            y, x, c, r = cv2.boundingRect(cnt)
            if not (35 < r < row - 25 and 35 < c < col - 25):
                cv2.fillConvexPoly(img, cnt, 0)
            # end if
        # end for
    # end for

    # check mean white pixels
    if np.mean(img) < 4:
        return None
    # end if

    return auto_crop(img)
# end function


def apply_flood_fill(img, region, tx=0, ty=0):
    row, col = img.shape
    mask = np.zeros((row + 2, col + 2), np.uint8)
    for x, _ in enumerate(region):
        for y, c in enumerate(_):
            if c > 0:
                cv2.floodFill(img, mask, (ty + y, tx + x), 0)
            # end if
        # end for
    # end for
    return img
# end function