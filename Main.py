# -*- coding: utf-8 -*-

import alpr
from modules import util


def main(argv):

    stages = []

    if len(argv) == 1:      # no input given
        # all stages sequentially
        stages = range(1, len(alpr.STAGE_MAP) + 1)

    elif len(argv) == 2:    # either a range or single stage
        try:
            if ':' not in argv[1]:  # single stage
                stages = [int(argv[1])]
            else:                   # range of stages

                start, stop = argv[1].split(':')
                if len(start) == 0:
                    start = 1
                else:
                    start = int(start)
                # end if
                if len(stop) == 0:
                    stop = len(alpr.STAGE_MAP) + 1
                else:
                    stop = int(stop) + 1
                # end if
                stages = range(start, stop)
            # end if
        except err:
            pass
        # end try

    elif len(argv) > 2:     # specified stages in specific order
        for i in range(1, len(argv)):
            try:
                stages.append(int(argv[i]))
            except err:
                pass
            # end try
        # end for
    # end if

    # check if any input has been given
    if len(stages) == 0:
        # wrong number of arguments
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
