# -*- coding: utf-8 -*-

import os
import numpy as np
from os import path
from modules import config as cfg


def log(*args, stage=0, force=False):
    text = " ".join(args)
    if cfg.DEBUG or force:
        print(" " * stage + text)
    # end if
# end function


def split_file(file):
    """
    Split a file info filename and extension pair
    :param file: File to parse.
    :return: (filename, extension) pair
    """
    return path.splitext(path.split(file)[1])
# end function


def ensure_path(directory):
    """Ensures the given path to exist.
    :param directory: Path to ensure
    """
    if not os.path.exists(directory):
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

