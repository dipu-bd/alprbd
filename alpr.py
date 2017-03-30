# -*- coding: utf-8 -*-

from modules import *

# Mapping of Stage to Action
# TODO: use a dictionary instead of array
STAGE_MAP = [
    [Grayscale.run, 0, 1],
    [Rescale.run, 1, 2],
    [Sobel.run, 2, 3],
    [Gaussian.run, 3, 4],
    [Intensify.run, 4, 5],
    [MatchFilter.run, 5, 6],
    [LocatePlate.run, 6, 7],
    [ExtractPlate.run, 7, 8],
    [Sobel.run, 8, 9],
    [Closing.run, 9, 10],
    [Opening.run, 10, 11],
    [PlateNoise.run, 11, 12],
    [LocatePlate.run, 12, 13],
    [ExtractOriginal.run, 13, 14],
    [BlackWhite.run, 14, 15],
    # rotate
    # remove border
    # HorizontalSegment.run,
    # VerticalSegment.run,
    # Features.run,
    # neural network
]

# index number of most referenced stages
ORIGINAL = 0
GRAYSCALE = 1
RESCALED = 2
LOCATE_SCALED = 7
SCALED_PLATE = 8
ORIGIN_REGION = 14
ORIGINAL_PLATE = 15

def execute(stage):
    """
    Call the function to for given stage variable.    
    :param stage: Stage number
    :param images: (read, write) image file array
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if stage < 0 or stage >= len(STAGE_MAP):
        util.log("Unknown stage:", stage)
        return False
    # end if

    # execute the stage function for each image
    method = STAGE_MAP[stage]
    method[0](*method[1:])      # call using arguments

    util.log("Executed: ", util.name_of(STAGE_MAP[stage]), '\n')
    return True
# end function
