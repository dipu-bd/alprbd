# -*- coding: utf-8 -*-

import os

def ensurePath(path):
    if not os.path.exists(path):
        os.makedirs(path)
    #end if 
#end function