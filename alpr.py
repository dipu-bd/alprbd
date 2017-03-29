# -*- coding: utf-8 -*-

from modules import util
from modules import Grayscale
from modules import Rescale


# Mapping of Stage to Action
STAGE_MAP = {
    '0': Grayscale.apply,
    '1': Rescale.apply,

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

