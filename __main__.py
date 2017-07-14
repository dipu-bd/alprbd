"""
Generates and formats the entire dataset
"""

import os
from shutil import rmtree
import Generator
import Formatter
import config as cfg

if os.path.exists('dataset'):
    rmtree('dataset')

Generator.run()

Formatter.format_docs(cfg.DIGITS_PATH)
Formatter.format_docs(cfg.LETTERS_PATH)
Formatter.format_docs(cfg.CITY_PATH)
