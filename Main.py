# -*- coding: utf-8 -*-

import os
import alpr
from os import path


def main(argv):
    
    files = parse_args(argv)

    # no input is given
    if len(files) == 0:
        return display_actions()
    # end if

    # run all stages 
    time = 0
    for file in files:
        print()
        time += alpr.execute(file)
    # end for
    time /= len(files)
    
    print("Mean Total: %.3f seconds" % time)
# end main


def display_actions():
    """
    Displays the list of actions
    """
    print("Provide valid path of image files to execute.")
    print("HELP:    `python . <file names...>`") 
    print()
# end function


def parse_args(argv):
    if len(argv) == 1:
        return get_files(path.abspath('stages'))
    # end if

    files = []
    for file in argv[1:]:
        # check if exists
        f = path.abspath(file)
        if path.exists(f):
            files.append(f)
        # end if
    # end function
    return files
# end function


def get_files(folder):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """
    # Open all images 
    images = []    
    VALID = [".jpg", ".png", ".bmp"]
    for file in os.listdir(folder):
        name = file.lower()
        if name.startswith('.'):
            continue    # skip hidden files
        # end if

        _, ext = path.splitext(name)
        if ext.lower() in VALID:
            images.append(path.join(folder, name))  # image file
        # end if
    # end for 
    return images
# end function


