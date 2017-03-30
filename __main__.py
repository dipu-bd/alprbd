# -*- coding: utf-8 -*-

import sys

from Main import main
from helper import *

# ensure that working directory exists
util.ensure_path(cfg.WORK_PATH)

# start program
main(sys.argv)
