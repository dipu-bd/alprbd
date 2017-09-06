"""
Starting point of the system
"""

import os
import sys
from glob import glob
from shutil import rmtree
import config as cfg


def ensure_path(folder):
    """Create folder if not exists"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    # end if
# end def

def process(file):
    """Process files"""
    print(file)
# end def

def main():
    """Starts program"""
    arg = 'LPDB'
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
    # end if
    arg = os.path.abspath(arg)

    rmtree(cfg.OUT_PATH) # removes previous output dir

    if os.path.isdir(arg):
        for file in glob(arg + os.sep + '*.jpg'):
            process(file)
        # end for
    else:
        process(arg)
    # end if
# end def

if __name__ == '__main__':
    main()
# end if
