"""
Pre-process image
"""
import cv2
import alprbd.config as cfg

# ---------- Clip Limited Adaptive Histogram Enhancement Function -----------
# http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
CLAHE = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(20, 40))


def process(frame):
    """
    Process img in order to make alpr-task easier
    :param frame: Image object
    :return: Image object after processing
    """
    frame.scaled = rescale(frame.original, cfg.SCALE_DIM)
    frame.gray = cv2.cvtColor(frame.scaled, cv2.COLOR_BGR2GRAY)
    frame.enhanced = CLAHE.apply(frame.gray)
    return frame
# end function


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


def get_binaries(region):
    """
    gets two binary images from the given region
    :param region: Region object
    :return: binary, and inverse binary image array
    """
    # process image
    img = region.image
    img = rescale(img, cfg.PLATE_DIM)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = CLAHE.apply(img)

    _, binary1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)

    return [binary1, binary2]
# end function
