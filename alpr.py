# -*- coding: utf-8 -*-

from modules import util


STAGE_MAP = {}


def execute(stage):
    """
    Call the function to for given stage variable.    
    :param stage: Must contain an ID and an images array.
    :return: True if success, False otherwise.
    """
    # check if stage is valid
    if stage['id'] not in STAGE_MAP:
        util.log("Unknown stage:", stage['id'])
        return False
    # end if

    # execute the stage function for each image
    f = STAGE_MAP[stage['id']]
    for read, write in stage['images']:
        f(read, write)
        util.log("Executed:", stage['id'], 'for', read, stage=stage['id'])
    # end for

    return True
# end function

