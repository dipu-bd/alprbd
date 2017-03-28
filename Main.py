#!/usr/bin/python

import cv2
from os import path
import modules.util as util
import modules.config as cfg 

import Grayscale
import Sobel


# Define working directory
WORK_PATH = path.join(path.curdir, "stages")
util.ensure_path(WORK_PATH)


def openStage(stage = 0):
    """Open an stage by stage number
    :param stage: Stage number to open 
    :return: An array of stage objects
    """
    path.join(WORK_PATH,
#end function

def main(imgFile, stage):

    for i in range(0, 2):
        if(isinstance(x, (int)) && i != stage):
            continue;
        #end if
        perform()
           
    #1 read image
    img = cv2.imread(imgFile)
    
    ##### Stage 2 ##### 
    #1 read original image
    img = cv2.imread(imgFile)
    #2 to grayscale        
    gray = Grayscale.apply(original.image) 
    stage1 = Stage('original', gray)
    stage1.save();
    
    ##### Stage 2 #####
    #1 rescale 
    scaled = Rescale.apply(gray.img)
    #2 apply sobel
    sobel = Sobel.apply(scaled)
    #3 apply gauss filter
    gauss = Gauss.apply(sobel), tools.build_blur_kernel())
    
    
    

# end main

# delete if exists
if os.path.exists(STAGE_PATH):
    #call(["rm", "-rf", STAGE_PATH])
#end if

if __name__ == "__main__":
    main(sys.argv[2], sys.argv[3])

