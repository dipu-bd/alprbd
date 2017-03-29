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
from modules import CropPlate
from modules import ExtractPlate
from modules import BlackWhite
from modules import HorizontalSegment
from modules import VerticalSegment
from modules import Features
from modules import PlateNoise

# Mapping of Stage to Action
STAGE_MAP = [
    Grayscale.run,          # 1
    Rescale.run,            # 2
    Sobel.run,              # 3
    Gaussian.run,           # 4
    Intensify.run,          # 5
    MatchFilter.run,        # 6
    LocatePlate.run,        # 7
    Sobel.run,              # 8
    Closing.run,            # 9
    Opening.run,            # 10
    PlateNoise.run,         # 11

    CropPlate.run,          # 12
    ExtractPlate.run,       # 13
    BlackWhite.run,         # 14
    # remove border
    # rotate
    HorizontalSegment.run,  # 15
    VerticalSegment.run,    # 16
    Features.run,           # 17
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
    util.log("Executed: ", util.function_name(STAGE_MAP[stage]), '\n')

    return True
# end function

