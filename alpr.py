# -*- coding: utf-8 -*-

import cv2
from modules import *

# Mapping of Stage to Action
# Elements: [function reference, previous stage, current stage, other arguments...]
STAGE_MAP = [
    # pre-processing             # STEP-A #
    [Grayscale.run, 0, 1],          # 1
    [Rescale.run, 1, 2],            # 2
    [Sobel.run, 2, 3],              # 3
    [Gaussian.run, 3, 4],           # 4
    [Intensify.run, 4, 5, 2],       # 5

    # plate detection            # STEP-B #
    [MatchFilter.run, 5, 6],        # 6
    [LocatePlate.run, 6, 7, 5],     # 7
    [Sobel.run, 7, 8],              # 8
    [Closing.run, 8, 9],            # 9
    [Opening.run, 9, 10],           # 10   

    # cleaning plate             # STEP-D #
    [PlateNoise.run, 11, 12, 8],    # 12
    [LocatePlate.run, 12, 13],      # 13
    [Extract.run, 13, 14, 7, 1],    # 14
    [BlackWhite.run, 14, 15],       # 15

    # segmentation


    # character recognition
    [Features.run, 100, 101],

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
    """
    # check if stage is valid
    if stage <= 0 or stage > len(STAGE_MAP):
        util.log("Unknown stage:", stage)
        return display_actions()
    # end if

    # execute the stage function for each image
    start = cv2.getTickCount()  # start time

    method = STAGE_MAP[stage - 1]
    method[0](*method[1:])      # call using arguments

    stop = cv2.getTickCount()   # end time
    time = (stop - start) / cv2.getTickFrequency()
    util.log("Executed in {:.3} seconds\n".format(time))
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
