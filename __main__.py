"""
Generates and formats the entire dataset
"""

import Generator
import Formatter
import config as cfg

Generator.run()

Formatter.format_docs(cfg.DIGITS_PATH)
Formatter.format_docs(cfg.LETTERS_PATH)
Formatter.format_docs(cfg.CITY_PATH)
