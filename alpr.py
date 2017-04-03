# -*- coding: utf-8 -*-

from helper import *
from modules import *

# Mapping of Stage to Action
# Elements: [function reference, previous stage, current stage, other arguments...]
STAGE_MAP = [
    # pre-processing             # STEP-A #
    [Rescale.run, 0, 1],            # 1
    [Grayscale.run, 1, 2],          # 2
    [Sobel.run, 2, 3],              # 3
    [Gaussian.run, 3, 4],           # 4
    [Intensify.run, 4, 5, 2],       # 5
    [MatchFilter.run, 5, 6],        # 6
    [PlateRegion.run, 6, 7],        # 7 *
    [LocatePlate.run, 7, 8, 0],     # 8 *

    # plate detection            # STEP-B #
    [Grayscale.run, 8, 9],           # 9
    [Threshold.run, 9, 10],          # 10 *
    [Canny.run, 10, 11],             # 11 *
    [Contours.run, 11, 12, 10],      # 12 **
    [ExtractPlate.run, 12, 13, 10],  # 13 **

    # character segmentation     # STEP-C #
    [BlackWhite.run, 13, 14],        # 14 **
    [BorderRemoval.run, 14, 15],     # 15 **
    [Denoise.run, 15, 16],           # 16 **
    [Segments.run, 16, 17],          # 17 ***

    # character recognition      # STEP-D #

    # combining result           # STEP-E #
]


def execute(stage):
    """
    Call the function to for given stage variable.    
    :param stage: Stage number
    """
    # execute the stage function for each image
    method = STAGE_MAP[stage - 1]

    util.delete_stage(method[2])    # delete current stage folder
    time = method[0](*method[1:])   # call using arguments

    util.log("Average execution time: %.3f seconds\n" % time)
    return time
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

    print("Example usage:")
    print("\tpython . <stage>")
    print(" :Executes the stage.")
    print("\tpython . <space separated stage numbers>")
    print(" :Executes each stages on list.")
    print("\tpython . <stage1>-<stage2>")
    print(" :Executes stages between stage1 and stage2 (inclusive).")
    print("\tpython . <stage>-")
    print(" :Executes all stages starting from given stage.")
    print("\tpython . -<stage1>")
    print(" :Executes all stages 1 to given stage.")

# end function
