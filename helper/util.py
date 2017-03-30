# -*- coding: utf-8 -*-

import os
import shutil
from os import path

import cv2
import numpy as np

from helper import config as cfg

VALID_DATA = [".txt"]
VALID_IMAGE = [".jpg", ".png", ".bmp"]


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
    tol = 355
    maxi = np.max(img)
    if maxi > tol:
        img = 255 * (img - (tol - 255)) / maxi
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

    # Open all images
    data = []
    images = []
    global VALID_DATA, VALID_IMAGE
    for file in os.listdir(folder):
        name = file.lower()
        if name.startswith('.'):
            continue    # skip hidden files
        # end if

        _, ext = path.splitext(name)
        if ext.lower() in VALID_IMAGE:
            images.append(name)  # image file
        elif ext.lower() in VALID_DATA:
            data.append(name)    # data file
        # end if
    # end for

    # for debugging
    if len(images):
        log(len(images), 'images', 'found on stage', stage)
    # end if
    if len(data):
        log(len(data), 'data', 'found on stage', stage)
    # end if

    return images, data
# end function


def delete_stage(stage):
    """
    Deletes a stage folder
    :param stage: 
    :return: 
    """
    folder = stage_folder(stage)
    shutil.rmtree(folder)  # delete old
    ensure_path(folder)    # create new
# end if


def name_of(func):
    """
    Retrieves the full name of the function
    :param func: Function name
    :return: 
    """
    folder = func.__code__.co_filename
    file = path.split(folder)[1]
    file = ".".join(path.splitext(file)[:-1])
    return file
# end function


def execute_module(method, *args):
    """
    
    :param method: 
    :param args: 
    :return: 
    """
    # get result
    start = cv2.getTickCount()
    result = method(*args)
    time = cv2.getTickCount() - start
    time /= cv2.getTickFrequency()
    return result, time
# end function
