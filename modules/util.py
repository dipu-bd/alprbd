# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from os import path
from modules import config as cfg

VALID_DATA = [".npy"]
VALID_IMAGE = [".jpg", ".gif", ".png", ".bmp"]


def log(*args, stage=None, force=False):
    if not (cfg.DEBUG or force):
        return
    # end if

    out = ""
    for i in args:
        out += " " + str(i)
    # end if

    if stage is not None:
        out = "> [" + str(stage+1) + "]: " + out
    else:
        out = "> " + out
    # end if

    print(out)
# end function


def ensure_path(directory):
    """Ensures the given path to exist.
    :param directory: Path to ensure
    """
    if not path.exists(directory):
        os.makedirs(directory)
    # end if
# end function


def stage_folder(stage_no):
    """
    Get stage folder from stage number
    :param stage_no: Stage number
    :return: A valid folder
    """
    name = "stage.{}".format(stage_no)
    folder = path.join(cfg.WORK_PATH, name)
    ensure_path(folder)
    return folder
# end function


def stage_image(filename, stage):
    """
    Get another stage's file from given
    :param filename: Current file name
    :param stage: Stage number
    :return: Full path of the image file
    """
    name, ext = path.splitext(filename)
    if ext in VALID_DATA:
        filename = name
    # end if
    return path.join(stage_folder(stage), filename)
# end function


def stage_data(filename, stage):
    """
    Get another stage's file from given
    :param filename: Current file name
    :param stage: Stage number
    :return: Full path of the data file
    """
    name, ext = path.splitext(filename)
    if ext not in VALID_DATA:
        filename += VALID_DATA[0]
    # end if
    return path.join(stage_folder(stage), filename)
# end function


def normalize(img):
    """Rounds to nearest integer and clears out-of-boundary values.
    Intensity boundary is [0, 255].
    :param img: Image to apply normalize
    """
    # maxi = np.max(img)
    # if maxi > 512:
    #     img *= 512.0 / maxi
    # # end if

    img = 255 * img / np.max(img)

    norm = np.round(img)
    norm[norm < 0] = 0
    norm[norm > 255] = 255

    return norm
# end function


def get_images(stage=0):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """
    return get_files(stage)[0]
# end function


def get_data(stage=0):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """
    return get_files(stage)[1]
# end function


def get_files(stage):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """

    # get folder
    folder = stage_folder(stage)

    # folder to write
    folder2 = stage_folder(stage + 1)
    shutil.rmtree(folder2) # delete old
    ensure_path(folder2)   # create new

    # Open all images
    data = []
    images = []
    global VALID_DATA, VALID_IMAGE
    for file in os.listdir(folder):
        name = file.lower()
        if name.startswith('.'):
            continue    # don't process hidden files
        # end if

        _, ext = path.splitext(name)
        if ext in VALID_IMAGE:
            images.append(name)  # image file
        elif ext in VALID_DATA:
            data.append(name)    # data file
        # end if
    # end for

    log(len(images), 'images +', len(data), 'data found on stage', stage)

    return images, data
# end function


def name_of(func):
    """
    Retrieves the full name of the function
    :param func: Function name
    :return: 
    """

    folder = func.__code__.co_filename
    file = path.split(folder)[1]
    file = ".".join(path.splitext(file)[:-1])
    return "{}.{}()".format(file, func.__name__)
# end function
