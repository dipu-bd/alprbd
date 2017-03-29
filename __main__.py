# -*- coding: utf-8 -*-

import sys
from Main import main
from modules import util
from modules import config as cfg

# ensure that working directory exists
util.ensure_path(cfg.WORK_PATH)

# start program
main(sys.argv)
