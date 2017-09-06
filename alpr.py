"""
Starting point of the system
"""

import os
import sys
from glob import glob
from shutil import rmtree
import config as cfg

from node import Node, Var
from skimage.io import imread
from skimage.transform import resize


def ensure_path(folder):
    """Create folder if not exists"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    # end if
# end def

def process(file):
    """Process files"""
    IMAGE = 'jpg'
    ARRAY = 'txt'

    op = dict()
    op['open'] = Node(imread, Var(file), ext=IMAGE)
    op['resize'] = Node(resize, op['open'], Var(480, 640), mode='wrap', ext=IMAGE)

    base = os.path.basename(file)
    print(base + ' ', end='')

    name = os.path.splitext(base)[0]
    out = os.path.join(cfg.OUT_PATH, name)
    ensure_path(out)

    index = 0
    for key in op:
        index += 1
        dest = os.path.join(out, "{0:02}_{1}".format(index, key))
        op[key].execute()
        op[key].save(dest)
        print('.', end='')
    # end for

    print('done')
# end def

def main():
    """Starts program"""
    arg = 'LPDB'
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
    # end if
    arg = os.path.abspath(arg)

    # if os.path.exists(cfg.OUT_PATH):
    #     rmtree(cfg.OUT_PATH) # removes previous output dir
    # # end if

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
