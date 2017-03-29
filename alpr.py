# -*- coding: utf-8 -*-

from modules import util
from modules import Grayscale
from modules import Rescale
from modules import Sobel
from modules import Gaussian


# Mapping of Stage to Action
STAGE_MAP = {
    '0': Grayscale.apply,
    '1': Rescale.apply,
    '2': Sobel.apply,
    '3': Gaussian.apply,
    # '4': intensify (stage.1, stage.3)
    # '5': sobel + matched + smoothing + threshold
    # '6': extract plate like regions (save image & region data)
    # '7': apply sobel
    # '8': morph opening
    # '9': morph closing
    # '10': apply dilation
    # '11': final check + extraction (stage.6.data, stage.1)
    # '12': convert black and white
    # '13': remove border
    # '14': rotate
    # '15': horizontal segmentation
    # '16': vertical segmentation
    # '17': feature extraction
    # '18': neural network

}


def execute(stage, images):
    """
    Call the function to for given stage variable.    
    :param stage: Stage number
    :param images: (read, write) image file array
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if str(stage) not in STAGE_MAP:
        util.log("Unknown stage:", stage)
        return False
    # end if

    # execute the stage function for each image
    func = STAGE_MAP[str(stage)]
    for read, write in images:
        func(read, write)
        util.log("Executed:", stage, stage=stage)
    # end for

    return True
# end function

