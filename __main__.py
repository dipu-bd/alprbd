# -*- coding: utf-8 -*-

import sys
from Main import main
from modules import util

# ensure that working directory exists
util.ensure_path(cfg.WORK_PATH)

# start program
if __name__ == "__main__":
    main(sys.argv)
# end if
