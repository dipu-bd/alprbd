"""
Starting point of the system
"""

import os
import sys
from glob import glob

def process(*files):
    """Process files"""
    print(files)
# end def

def main():
    """Starts program"""
    arg = os.path.abspath(sys.argv[1] or 'LPDB')

    if os.path.isdir(arg):
        process(glob(arg + os.sep + '*.jpg'))
    else:
        process(arg)
    # end if
# end def

if __name__ == '__main__':
    main()
# end if
