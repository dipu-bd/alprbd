# -*- coding: utf-8 -*-

from modules import util
from modules import Grayscale
from modules import Rescale
from modules import Sobel
from modules import Gaussian


# Mapping of Stage to Action
STAGE_MAP = [
    Grayscale.apply,
    Rescale.apply,
    Sobel.apply,
    Gaussian.apply,
    # intensify (stage.1, stage.3)
    # sobel + matched + smoothing + threshold
    # extract plate like regions (save image & region data)
    # apply sobel
    # morph opening
    # morph closing
    # apply dilation
    # final check + extraction (stage.6.data, stage.1)
    # convert black and white
    # remove border
    # rotate
    # horizontal segmentation
    # vertical segmentation
    # feature extraction
    # neural network
]


def execute(stage, images, data):
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
    func = STAGE_MAP[stage]

    if len(images) > 0:
        for file in images:
            func(file, stage + 1)
            util.log("Executed by image", stage=stage)
        # end for
    elif len(data) > 0:
        for file in data:
            func(file, stage + 1)
            util.log("Executed by data", stage=stage)
        # end for
    else:
        util.log("No file to execute", stage=stage)
        return False
    # end if

    return True
# end function

