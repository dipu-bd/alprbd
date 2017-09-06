""" Unlicensed """
import re
import cv2
import numpy as np


class Node:
    """An unit of operation"""

    def __init__(self, func, *args, ext=None, foreach=False, **kargs):
        self.func = func
        self.args = args
        self.kargs = kargs
        self.result = None
        self.extension = ext
        self.foreach = foreach
    # end def

    def get(self):
        return self.result
    # end def

    def execute(self):
        """Execute the node"""
        if self.result is None:
            args = [x.get() for x in self.args]
            if not self.foreach:
                self.result = self.func(*args, **self.kargs)
            else: 
                self.result = []
                for inp in args[0]:
                    parg = [ inp ].extend(args[1:])
                    self.result.append(self.func(*parg, **self.kargs))
                # end for
            # end if
        # end if
    # end def

    def save(self, filename):
        """Store result to file"""
        if self.extension is None:
            return False
        # end if
        filename = filename + '.' + self.extension
        if re.match('jpg|bmp|png', self.extension):
            cv2.imwrite(filename, self.result)
        elif self.extension == 'txt':
            np.savetxt(filename, self.result)
        else:
            np.save(filename, self.result)
        # end if
        return True
    # end def
# end class


class Var:
    """Decalare a variable"""

    def __init__(self, *val):
        if len(val) == 0:
            self.val = None
        elif len(val) == 1:
            self.val = val[0]
        else:
            self.val = tuple(val)
        # end if
    # end def

    def get(self):
        """Get the value"""
        return self.val
    # end def

    def set(self, val):
        """Set te value"""
        self.val = val
    # end def

# end class
