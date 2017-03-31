# -*- coding: utf-8 -*-

import alpr
from helper import util


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
    time = 0
    for stage in stages:
        time += alpr.execute(stage)
    # end for
    print("Mean Total: %.3f seconds" % time)
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
    # no input is given
    if len(argv) == 1:
        # all stages sequentially
        return range(1, len(alpr.STAGE_MAP) + 1)
    # end if

    stages = []
    for i in range(1, len(argv)):
        start = 1
        stop = len(alpr.STAGE_MAP)

        if '-' not in argv[i]:    # single stage
            start = stop = get_stage(argv[i])
        elif argv[i][0] == '-':   # from beginning
            stop = get_stage(argv[i][1:])
        elif argv[i][-1] == '-':  # until end
            start = get_stage(argv[i][:-1])
        else:   # range of stages
            start, stop = argv[1].split('-')
            start = int(start)
            stop = int(stop)
        # end if

        stages.extend(range(start, stop + 1))
    # end for
    return stages

# end function
