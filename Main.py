# -*- coding: utf-8 -*-

import alpr
from modules import util


def main(argv):

    stages = []

    try:
        stages = parse_argv(argv)
    except:
        pass
    # end try

    # check if any input has been given
    if len(stages) == 0:
        util.log("Invalid number of arguments")
        return alpr.display_actions()
    # end if

    # run all stages
    print()
    for stage in stages:
        alpr.execute(stage)
    # end for
    print("\nSUCCESS.")

# end main


def get_stage(arg):
    # check if stage is valid
    stage = int(arg)
    if stage <= 0 or stage > len(alpr.STAGE_MAP):
        util.log("Unknown stage:", stage)
        raise Exception("Unknown stage")
    # end if
    return stage
# end function


def parse_argv(argv):
    """
    Parses the input arguments and get a list of stages
    :param argv: 
    :return: 
    """
    stages = []

    if len(argv) == 1:  # no input given
        # all stages sequentially
        stages = range(1, len(alpr.STAGE_MAP) + 1)

    elif len(argv) == 2:  # either a range or single stage
        if ':' not in argv[1]:  # single stage
            stages = [get_stage(argv[1])]
        else:  # range of stages

            start, stop = argv[1].split('-')
            if len(start) == 0:
                start = 1
            else:
                start = get_stage(start)
            # end if
            if len(stop) == 0:
                stop = len(alpr.STAGE_MAP) + 1
            else:
                stop = get_stage(stop) + 1
            # end if
            stages = range(start, stop)
            # end if

    elif len(argv) > 2:  # specified stages in specific order
        for i in range(1, len(argv)):
            stages.append(get_stage(argv[i]))
        # end for
    # end if

    return stages
# end function
