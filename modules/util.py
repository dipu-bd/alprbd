# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from os import path
from modules import config as cfg


def log(*args, stage=None, force=False):
    if not (cfg.DEBUG or force):
        return
    # end if

    out = ""
    for i in args:
        out += " " + str(i)
    # end if

    if stage is not None:
        out = "> [" + str(stage) + "]: " + out
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


def stage_file(filename, stage):
    """
    Get another stage's file from given
    :param filename: Current file name
    :param stage: Stage number
    :return: Full path of the file
    """
    return path.join(stage_folder(stage), filename)
# end function


def normalize(img):
    """Rounds to nearest integer and clears out-of-boundary values.
    Intensity boundary is [0, 255].
    :param img: Image to apply normalize
    """
    maxi = np.max(img)
    if maxi > 512:
        img *= 512.0 / maxi
    # end if

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
    valid_data = [".mat"]
    valid_images = [".jpg", ".gif", ".png", ".bmp"]
    for file in os.listdir(folder):
        name = file.lower()
        _, ext = path.splitext(name)
        if ext in valid_images:
            images.append(name)  # image file
        elif ext in valid_data:
            data.append(name)    # data file
        # end if
    # end for

    log(len(images), 'images +', len(data), 'data found on stage', stage)

    return images, data
# end function


def other_stage_file(file, stage, other_stage=None, other_ext=None):
    """
    Get another stage's file from given
    :param file: Current file name
    :param stage: Current stage number
    :param other_stage: Other stage number. Default is stage + 1
    :param other_ext: Extension of stage file. Default is current extension.
    :return: 
    """
    # split given file
    file = file.lower()
    name, ext = path.splitext(file)

    if other_ext is None:
        other_ext = ext
    # end if
    if not other_ext.startswith("."):
        other_ext = "." + other_ext
    # end if

    if other_stage is None:
        other_stage = int(stage) + 1
    # end if

    return stage_file(file + other_ext, other_stage)
# end function


def function_name(func):
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