# -*- coding: utf-8 -*-

import alpr
from modules import util


def main(argv):

    if len(argv) == 2:
        # run specific stage
        alpr.execute(int(argv[1]))

    elif len(argv) == 1:
        # run all stages sequentially
        for i in range(0, len(alpr.STAGE_MAP)):
            alpr.execute(i)
        # end for

    else:
        # wrong number of arguments
        util.log("Invalid number of arguments")
    # end if

    print("\nSUCCESS.")

# end main
