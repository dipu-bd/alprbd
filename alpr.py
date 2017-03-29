# -*- coding: utf-8 -*-

from modules import util
from modules import Grayscale
from modules import Rescale
from modules import Sobel
from modules import Gaussian
from modules import Intensify
from modules import MatchFilter
from modules import LocatePlate
from modules import Opening
from modules import Closing
from modules import ExtractOriginal
from modules import ExtractPlate
from modules import PlateNoise
from modules import BlackWhite
from modules import Threshold
from modules import HorizontalSegment
from modules import VerticalSegment
from modules import Features
from modules import Erosion

# Mapping of Stage to Action
# TODO: use a dictionary instead of array
STAGE_MAP = [
    Grayscale.run,          # 1
    Rescale.run,            # 2
    Sobel.run,              # 3
    Gaussian.run,           # 4
    Intensify.run,          # 5
    MatchFilter.run,        # 6
    LocatePlate.run,        # 7
    ExtractPlate.run,       # 8
    Sobel.run,              # 9
    Closing.run,            # 10
    Opening.run,            # 11
    PlateNoise.run,         # 13
    LocatePlate.run,        # 14
    ExtractOriginal.run,    # 15
    BlackWhite.run,         # 16

    # remove border
    # rotate
    #HorizontalSegment.run,  # 15
    #VerticalSegment.run,    # 16
    #Features.run,           # 17
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
    if stage < 0 or stage >= len(STAGE_MAP):
        util.log("Unknown stage:", stage)
        return False
    # end if

    # execute the stage function for each image
    STAGE_MAP[stage](stage)

    util.log("Executed: ", util.name_of(STAGE_MAP[stage]), '\n')

    return True
# end function
