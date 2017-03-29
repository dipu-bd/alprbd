# -*- coding: utf-8 -*-

import os
import numpy as np
from os import path
from modules import config as cfg


def log(*args, stage=0, force=False):
    if cfg.DEBUG or force:
        if stage > 0:
            print("  [", stage, "]", args)
        else:
            print('> ', args)
        #end if
    # end if
# end function


def get_file(current, stage=None, ext=None):
    """
    Get another stage's file from given
    :param current: 
    :param stage:
    :param ext: 
    :return: 
    """
    # split given file
    folder, file = path.split(current.lower())
    name, cur_ext = path.splitext(file)

    if ext is None:
        ext = cur_ext
    # end if
    if not ext.startswith("."):
        ext = "." + ext
    # end if

    cur = folder.split('.')[-1]
    if stage is None:
        stage = int(cur) + 1
    # end if

    new = path.dirname(folder)
    new = path.join(new, 'stage.' + str(stage))
    ensure_path(new)

    return path.join(new, file + ext)
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

