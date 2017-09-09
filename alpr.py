"""
Starting point of the system
"""

import os
import sys
import cv2
from glob import glob
from shutil import rmtree

import config as cfg
from node import Var
from opencv_model import Model


def ensure_path(folder):
    """Create folder if not exists"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    # end if
# end def

def process(file):
    """Process files"""
    gm = Model()
    gm['_file'].set(file)

    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    out = os.path.join(cfg.OUT_PATH, name)
    ensure_path(out)

    print(base, end='\n')
    index = 0
    total = 0
    for key in gm:
        if key[0] == '_':
            continue
        # end if
        #print('\t', index, key, end='')
        index += 1
        dest = os.path.join(out, "{0:02}_{1}".format(index, key))
        
        start = cv2.getTickCount()
        gm[key].execute()
        time = cv2.getTickCount() - start
        time /= cv2.getTickFrequency()
        total += time

        gm[key].save(dest)
        print('  ', key.title(), '& $%.4f$' % time)
    # end for
    print('==== %.4f' % total, '====\n')
    return total
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
        time = 0
        files = glob(arg + os.sep + '*.jpg')
        for file in files:
            time += process(file)
        # end for
        avg = time / len(files)
        print('==========================')
        print('Average = ', ' %.4f' % avg)
    else:
        process(arg)
    # end if
# end def

if __name__ == '__main__':
    main()
# end if
