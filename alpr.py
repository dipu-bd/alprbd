# -*- coding: utf-8 -*-

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
    [MatchFilter.run, 5, 6],        # 6

    # plate detection            # STEP-B #
    [LocatePlate.run, 6, 7, 5],     # 7
    [Sobel.run, 7, 8],              # 8
    [Closing.run, 8, 9],            # 9
    [Opening.run, 9, 10],           # 10
    [Dilation.run, 10, 11, 3],      # 11

    [Contours.run, 11, 12, 7],      # 12

    # cleaning plate             # STEP-D #
    # [PlateNoise.run, 11, 12, 8],    # 12
    # [LocatePlate.run, 12, 13],      # 13
    # [Extract.run, 13, 14, 7, 1],    # 14
    # [BlackWhite.run, 14, 15],       # 15

    # segmentation

    # character recognition
    # [Features.run, 100, 101],

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
