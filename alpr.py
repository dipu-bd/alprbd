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
    arg = 'LPDB'
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
    # end if
    arg = os.path.abspath(arg)

    if os.path.isdir(arg):
        process(glob(arg + os.sep + '*.jpg'))
    else:
        process(arg)
    # end if
# end def

if __name__ == '__main__':
    main()
# end if
