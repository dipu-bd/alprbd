# -*- coding: utf-8 -*-

from modules import util


STAGE_MAP = {}


def execute(stage, images):
    """
    Call the function to for given stage variable.    
    :param stage: Stage number
    :param images: (read, write) image file array
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if stage not in STAGE_MAP:
        util.log("Unknown stage:", stage)
        return False
    # end if

    # execute the stage function for each image
    f = STAGE_MAP[stage]
    for read, write in images:
        f(read, write)
        util.log("Executed:", stage, stage=stage)
    # end for

    return True
# end function

