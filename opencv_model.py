""" Unlicensed """
from collections import OrderedDict
import cv2
import numpy as np
from node import Node, Var
from skimage.transform import radon
from skimage.segmentation import clear_border

IMAGE = 'jpg'
ARRAY = 'txt'

def Model():
    """Get an operational model"""
    m = OrderedDict()
    m['_file'] = Var(None)
    m['open'] = Node(cv2.imread, m['_file'], ext=IMAGE)
    m['resize'] = Node(rescale, m['open'], Var(640), ext=IMAGE)
    m['gray'] = Node(to_gray, m['resize'], ext=IMAGE)
    m['clahe'] = Node(apply_clahe, m['gray'], Var(30, 60), Var(2.3), ext=IMAGE)
    m['sobel'] = Node(cv2.Sobel, m['clahe'], Var(-1), Var(1), Var(0), ksize=3, ext=IMAGE)
    m['thresh_sobel'] = Node(threshold, m['sobel'], Var(100), Var(255), Var(cv2.THRESH_TOZERO), ext=IMAGE)
    m['match_filter'] = Node(match_filter, ext=ARRAY)
    m['matched'] = Node(cv2.filter2D, m['thresh_sobel'], Var(-1), m['match_filter'], ext=IMAGE)
    m['blur'] = Node(cv2.GaussianBlur, m['matched'], Var(15, 15), Var(0), ext=IMAGE)
    m['thresh_blur'] = Node(threshold, m['blur'], Var(180), Var(255), Var(cv2.THRESH_TOZERO), ext=IMAGE)
    m['contours'] = Node(contours, m['thresh_blur'], Var(cv2.RETR_TREE))
    m['bounds'] = Node(bounding_rect, m['contours'], each=True)
    m['extract'] = Node(translate_point, m['bounds'], m['resize'], m['open'], each=True, ext=IMAGE)
    m['gray_plate'] = Node(to_gray, m['extract'], each=True, ext=IMAGE)
    m['clahe_plate'] = Node(apply_clahe, m['gray_plate'], Var(5, 5), Var(1.0), ext=IMAGE, each=True)
    m['bilateral'] = Node(cv2.bilateralFilter, m['clahe_plate'], Var(7), Var(25), Var(50), ext=IMAGE, each=True)
    m['sobel_plate'] = Node(cv2.Sobel, m['bilateral'], Var(-1), Var(0), Var(1), ksize=3, ext=IMAGE, each=True)
    m['thresh_sobel_plate'] = Node(threshold, m['sobel_plate'], Var(100), Var(255), Var(cv2.THRESH_TOZERO), ext=IMAGE, each=True)
    m['canny'] = Node(cv2.Canny, m['thresh_sobel_plate'], Var(200), Var(200), L2gradient=True, each=True, ext=IMAGE)
    m['resize_plate'] = Node(rescale, m['canny'], Var(180), ext=IMAGE, each=True)
    m['radon_t'] = Node(apply_radon, m['resize_plate'], each=True)
    m['radon'] = Node(smooth_radon, m['radon_t'], ext=IMAGE, each=True)
    m['angle'] = Node(find_angle, m['radon_t'], each=True, ext=ARRAY)
    m['rotate'] = Node(rotate_all, m['bilateral'], m['angle'])
    #m['combine'] = Node(combine, m['rotate'], m['bilateral'])
    m['trim'] = Node(trim_image, m['rotate'], each=True, ext=IMAGE)
    m['binary'] = Node(get_binary, m['trim'], each=True, ext=IMAGE)
    m['clear_border'] = Node(clear_border, m['binary'], each=True, ext=IMAGE)
    m['denoise'] = Node(denoise, m['clear_border'], each=True, ext=IMAGE)
    m['plate_trim'] = Node(trim_image, m['denoise'], each=True, ext=IMAGE)
    m['segments'] = Node(get_segments, m['plate_trim'], each=True)
    m['combine_char'] = Node(combine, m['segments'])
    m['char_trim'] = Node(trim_image, m['combine_char'], each=True, ext=IMAGE)
    m['resize_char'] = Node(resize, m['char_trim'], Var(28, 28), each=True, ext=IMAGE)

    return m
# end def

def match_filter():
    """
    Builds a gaussian match filter
    """
    # formula -- @article(joarder2012bangla)
    m, n = 12, 25           # window size
    A, B = 0.033, -0.012    # intensity
    sa, sb = 15.0, 10.0     # spreading

    a = 4  # 0 to a
    b = 6  # b to m

    x1 = 2
    x2 = a + 1
    x3 = b + 1

    X = np.arange(m)
    Y = np.arange(n)

    X1 = X[:a]
    X2 = X[a:b]
    X3 = X[b:]

    X1 = np.square((X1 - x1) / sa)
    X2 = np.square((X2 - x2))
    X3 = np.square((X3 - x3) / sb)

    H1 = A * np.exp(-X1 / 0.2)
    H2 = B * np.exp(-X2 / 2.0)
    H3 = A * np.exp(-X3 / 0.2)
    H = np.hstack((H1, H2, H3))

    _, kernel = np.meshgrid(Y, H)
    return kernel
# end function


def smooth_radon(img):
    img += np.min(img)
    img /= np.max(img)
    img *= 255
    return np.uint8(img)
# end def

def rescale(img, wid):
    """Resize image preserving aspect ratio"""
    row, col = img.shape[:2]
    return cv2.resize(img, (wid, wid * row // col))
# end def

def rescale2(img, hi):
    """Resize image preserving aspect ratio"""
    row, col = img.shape[:2]
    return cv2.resize(img, (hi * col // row, hi))
# end def

def resize(img, size):
    """Resize image preserving aspect ratio"""
    row, col = img.shape[:2]
    if 2 * row < col:
        return rescale2(img, size[0])
    return cv2.resize(img, size)
# end def

def to_gray(img):
    b, g, r = cv2.split(img)
    return np.uint8(0.299 * r + 0.587 * g + 0.114 * b)
# end def

def apply_clahe(img, kernel=(8, 8), clip=1.0):
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=kernel)
    return clahe.apply(img)
# end def

def threshold(*args, **kargs):
    return cv2.threshold(*args, **kargs)[1]
# end def

def contours(img, retr):
    return cv2.findContours(img, retr, cv2.CHAIN_APPROX_SIMPLE)[1]
# end def

def bounding_rect(cnt):
    """Get bounding box"""
    y, x, c, r = box = cv2.boundingRect(cnt)
    if r < c and 20 < r < 150 and 60 < c < 350:
        return box
    # end if
    return None
# end def

def translate_point(box, scaled, img):
    """translate points"""
    y, x, c, r = box
    scaled_height, scaled_width = scaled.shape[:2]
    height, width = img.shape[:2]

    x = (x * height) // scaled_height
    y = (y * width) // scaled_width
    r = (r * height) // scaled_height
    c = (c * width) // scaled_width

    x1 = max(0, x - 3)
    x2 = min(height, x + r + 7)
    y1 = max(0, y - 4)
    y2 = min(width, y + c + 9)

    return img[x1:x2, y1:y2]
# end def

def apply_radon(img):
    row, col = img.shape
    img[[0, row-1], :] = 0
    img[:, [0, col-1]] = 0
    theta = np.linspace(-90., 90., 180, endpoint=False)
    sinogram = radon(img, theta=theta, circle=True)
    return sinogram
# end def

def find_angle(sinogram):
    x, y = np.where(sinogram == sinogram.max())
    y = (90 - y[0]) % 90
    if y > 45: y = 90 - y
    return y
# end def

def rotate_all(imgs, angles):
    res = []
    for i, angle in enumerate(angles):
        img = imgs[i]
        if angle == 0:
            res.append(img)
            continue
        # end if
        row, col = img.shape
        center = tuple(np.array(img.shape) // 2)
        mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        out = cv2.warpAffine(img, mat, (col * 2, row * 2))
        res.append(out)
    # end for
    return res
# end def

def get_binary(img):
    """Converts to black and white / binary image"""
    # normal binary threshold
    bnw1 = cv2.threshold(np.uint8(img), 50, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    # inverse binary threshold
    bnw2 = cv2.threshold(np.uint8(img), 50, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    # calculate ratio of non-zero pixels
    if np.mean(bnw1) < np.mean(bnw2):
        return bnw1
    else:
        return bnw2
    # end if
# end function

def denoise(img):
    """Denoise image"""
    row, col = img.shape
    for cnt in contours(img.copy(), cv2.RETR_EXTERNAL):
        y, x, c, r = cv2.boundingRect(cnt)
        if not (25 < r < row - 25 and 25 < c < col - 25):
            cv2.fillConvexPoly(img, cnt, 0)
        # end if
    # end for

    # check mean white pixels
    if np.mean(img) < 4:
        return None
    # end if

    return img
# end def


def get_segments(img):
    """
    Calculate the horizontal projections.
    :param img: img to segment
    """
    # calculate horizontal projections
    hors = horizontal(img)

    # calculate vertical projections
    vers = []
    for x in hors:
        vers.extend(vertical(x))
    # end for

    return vers
# end function


def horizontal(img):
    """
    Calculate the horizontal segments.
    :param img: plate image
    """
    hor = []
    plate = None
    row_sum = np.mean(img, axis=1)
    for r, v in enumerate(row_sum):
        if v >= 1:
            if plate is None:
                plate = img[r:r+1, :]
            else:
                plate = np.vstack((plate, img[r:r+1, :]))
            # end if
        else:
            if isvalid(plate):
                hor.append(plate)
                plate = None
            # end if
        # end if
    # end for

    plate = trim_image(plate)
    if isvalid(plate):
        hor.append(plate)
    # end if

    return hor
# end if


def vertical(img):
    """
    Calculate the horizontal segments.
    :param img: plate image
    """
    ver = []
    plate = None
    col_sum = np.mean(img, axis=0)
    for c, v in enumerate(col_sum):
        if v >= 1:
            if plate is None:
                plate = img[:, c:c+1]
            else:
                plate = np.hstack((plate, img[:, c:c+1]))
            # end if
        else:
            if isvalid(plate):
                ver.append(plate)
                plate = None
            # end if
        # end if
    # end for

    plate = trim_image(plate)
    if isvalid(plate):
        ver.append(plate)
    # end if

    return ver
# end if


def isvalid(plate):
    """
    Checks whether the plate is valid
    :param plate:
    :return:
    """
    if plate is None:
        return False
    # end if

    row, col = plate.shape
    if row < 12 or col < 12:
        return False
    # end if

    if np.mean(plate) < 5:
        return False
    # end if

    return True
# end if


def trim_image(img):
    """Keep only important part"""
    # check image
    if img is None:
        return None
    # end if
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx) - 1)
    x2 = min(rows, np.max(nzx) + 3)
    y1 = max(0, np.min(nzy) - 1)
    y2 = min(cols, np.max(nzy) + 3)
    # crop
    return img[x1:x2, y1:y2]
# end function

def combine(*args):
    out = []
    for result in args:
        if hasattr(result, 'shape'):
            out.append(result)
        else:
            out.extend(combine(*result))
        # end if
    # end for
    return out
# end def

def recognize(segments):
    
# end def
