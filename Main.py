# -*- coding: utf-8 -*-

import alpr
from os import path
from helper import util


def main(argv):
    
    files = []
    for file in argv[1:]:
        # check if exists
        f = path.abspath(file)
        if path.exists(f):
            files.append(f)
        # end if
    # end function

    # no input is given
    if len(files) == 0:
        return display_actions()
    # end if

    # run all stages
    print()
    time = 0
    for file in files:
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
