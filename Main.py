# -*- coding: utf-8 -*-

import os
import alpr
import shutil
from modules import util
from modules import config as cfg


def main(*args):

    if len(args) == 2:
        # run specific stage
        run_stage(int(args[1]))

    elif len(args) == 1:
        # run all stages sequentially
        for key in alpr.STAGE_MAP:
            run_stage(int(key))
        # end for

    else:
        # wrong number of arguments
        util.log("Invalid number of arguments")
    # end if

    print("\nSUCCESS.")
# end main


def run_stage(stage_no):
    images, data = load_images(stage_no)
    alpr.execute(stage_no, images, data)
# end function


def load_images(stage=0):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """

    # get folder
    folder = os.path.join(cfg.WORK_PATH, 'stage.'+str(stage))

    # check folder
    if not os.path.exists(folder):
        util.log(folder, "does not exists")
        raise Exception("Input folder does not exists")
    # end if

    # folder to write
    folder2 = os.path.join(cfg.WORK_PATH, 'stage.' + str(stage + 1))
    shutil.rmtree(folder2)      # delete old
    util.ensure_path(folder2)   # create new

    # Open all images
    data = []
    images = []
    valid_data = [".mat"]
    valid_images = [".jpg", ".gif", ".png", ".bmp"]
    for file in os.listdir(folder):
        name, ext = util.split_file(file)
        if ext in valid_images:
            images.append(file)
        elif ext in valid_data:
            data.append(file)
        # end if
    # end for

    util.log(len(images), 'images &', len(data), 'data found on stage', stage)

    return images, data
# end function
