# -*- coding: utf-8 -*-

import cv2
from modules import *

# Mapping of Stage to Action
# Elements: [function reference, function arguments...]
STAGE_MAP = [
    [Grayscale.run, 0, 1],
    [Rescale.run, 1, 2],
    [Sobel.run, 2, 3],
    [Gaussian.run, 3, 4],
    [Intensify.run, 4, 5, 2],
    [MatchFilter.run, 5, 6],
    [LocatePlate.run, 6, 7],
    [ExtractPlate.run, 7, 8, 2],
    [Sobel.run, 8, 9],
    [Closing.run, 9, 10],
    [Opening.run, 10, 11],
    [PlateNoise.run, 11, 12, 8],
    [LocatePlate.run, 12, 13],
    [ExtractOriginal.run, 13, 14, 7, 1],
    [BlackWhite.run, 14, 15],
    # rotate
    # remove border
    # HorizontalSegment.run,
    # VerticalSegment.run,
    # Features.run,
    # neural network
]


def execute(stage):
    """
    Call the function to for given stage variable.    
    :param stage: Stage number
    :param images: (read, write) image file array
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if stage <= 0 or stage > len(STAGE_MAP):
        util.log("Unknown stage:", stage)
        display_actions()
        return False
    # end if

    # execute the stage function for each image
    start = cv2.getTickCount()  # start time

    method = STAGE_MAP[stage - 1]
    method[0](*method[1:])      # call using arguments

    stop = cv2.getTickCount()   # end time
    time = float(stop - start) / cv2.getTickFrequency()
    util.log("Executed in {0:.3} seconds".format(time))
    return True
# end function


def display_actions():
    """
    Displays the list of actions
    """
    print("Available stages:")
    for stage, action in enumerate(STAGE_MAP):
        print("  %2d/  %s (%d params)" %
              (stage + 1, util.name_of(action[0]), len(action) - 1))
    # end for
# end function
