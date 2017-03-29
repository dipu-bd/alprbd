# -*- coding: utf-8 -*-

from modules import util


STAGE_MAP = {}


def execute(id, images):
    """
    Call the function to for given stage variable.    
    :param stage: Must contain an ID and an images array.
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if id not in STAGE_MAP:
        util.log("Unknown stage:", id)
        return False
    # end if

    # execute the stage function for each image
    f = STAGE_MAP[id]
    for read, write in images:
        f(read, write)
        util.log("Executed:", id, stage=id)
    # end for

    return True
# end function

