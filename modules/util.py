# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from os import path
from modules import config as cfg


def log(*args, stage=0, force=False):
    if not (cfg.DEBUG or force):
        return
    # end if

    out = ""
    for i in args:
        out += " " + str(i)
    # end if

    if stage > 0:
        out = "  [" + str(stage) + "]" + out
    else:
        out = "> " + out
    # end if

    print(out)
# end function


def split_file(file):
    """
    Split a file info filename and extension pair
    :param file: File to parse.
    :return: (filename, extension) pair
    """
    return path.splitext(path.split(file.lower())[1])
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
    folder = os.path.join(cfg.WORK_PATH, 'stage.'+str(stage))

    # check folder
    if not os.path.exists(folder):
        log(folder, "does not exists")
        raise Exception("Input folder does not exists")
    # end if

    # folder to write
    folder2 = os.path.join(cfg.WORK_PATH, 'stage.' + str(stage + 1))
    if os.path.exists(folder2):
        shutil.rmtree(folder2)      # delete old
    # end if
    ensure_path(folder2)   # create new

    # Open all images
    data = []
    images = []
    valid_data = [".mat"]
    valid_images = [".jpg", ".gif", ".png", ".bmp"]
    for file in os.listdir(folder):
        name, ext = split_file(file)
        if ext in valid_images:
            images.append(file)
        elif ext in valid_data:
            data.append(file)
        # end if
    # end for

    log(len(images), 'images +', len(data), 'data found on stage', stage)

    return images, data
# end function


def stage_file(current, stage=None, ext=None):
    """
    Get another stage's file from given
    :param current: Current file name
    :param stage: What stage file to extract. Default is next stage.
    :param ext: Extension of stage file
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

