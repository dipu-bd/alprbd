# -*- coding: utf-8 -*-

import alpr
from modules import util


def main(argv):

    print()

    if len(argv) == 1:
        # run all stages sequentially
        for i in range(0, len(alpr.STAGE_MAP)):
            alpr.execute(i)
        # end for

    elif len(argv) >= 2:
        # check if help required
        if argv[1] == '-h':
            alpr.display_actions()
            return
        # end if

        # run all specified stages
        for i in range(0, len(argv) - 1):
            alpr.execute(int(argv[i + 1]) - 1)
        # end for

    else:
        # wrong number of arguments
        util.log("Invalid number of arguments")
    # end if

    print("\nSUCCESS.")

# end main
