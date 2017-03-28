# -*- coding: utf-8 -*-

from os import path;
from modules.util import ensurePath;

# path to save file of different sages
STAGE_PATH = path.join(path.curdir, 'out');
                         
class Stage:
        
    def __init__(self, name, image=None, _id=1):
        self.id = _id;
        self.name = name;
        self.image = image;
        self.path = 'stage-{}'.format(_id)
        self.path = path.join(STAGE_PATH, self.path)
        ensurePath(self.path)
    #end function                
        
    def next(self, name, image=None):
        s = Stage(name, image, self.id + 1)
        s.prev = self
        self.next = s
        return s
    #end function    

    def filename(self):
        self.file = path.join(self.path, self.name + ".png")
        return self.file
    #end function

# end class
    
