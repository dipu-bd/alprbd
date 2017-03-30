# -*- coding: utf-8 -*-

import alpr
from modules import util


def main(argv):

    stages = []

    if len(argv) == 1:
        # all stages sequentially
        stages = range(1, len(alpr.STAGE_MAP) + 1)

    elif len(argv) >= 2:
        # specified stages in specific order
        for i in range(1, len(argv)):
            try:
                stages.append(int(argv[i]))
            except err:
                pass
            # end try
        # end for
    # end if

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
