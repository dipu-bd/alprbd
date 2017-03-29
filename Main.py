# -*- coding: utf-8 -*-

import os
import alpr
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
    images = load_images(stage_no)
    alpr.execute(stage_no, images)
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

    # folder for next stage
    folder2 = os.path.join(cfg.WORK_PATH, 'stage.' + str(stage + 1))
    util.ensure_path(folder2)

    # Open all images
    images = []
    valid_images = ["jpg", "gif", "png", "bmp"]
    for read in os.listdir(folder):
        name, ext = util.split_file(read)
        if ext in valid_images:
            write = os.path.join(folder2, name + "." + ext)
            images.append((read, write))
        # end if
    # end for

    return images
# end function
