# -*- coding: utf-8 -*-

import os
from os import path

import cv2
import Segments
from Extraction import extract


def execute(file):
    """
    Execute the ALPR process
    :param stage: Stage number
    """ 
    total_time = 0

    # open file
    img = cv2.imread(file)    
    save_dir, _ = path.splitext(file)    
    save_image(img, save_dir, 'main.jpg') # save original

    # execute extraction
    print(file)
    print("   Extracting all plate like regions...")
    plates, time = execute_module(extract, img)
    total_time += time

    print("   Segmenting %d extracted plates..." % len(plates))
    for i, plate in enumerate(plates):
        # save plate
        plate_dir = path.join(save_dir, 'plate_{:02}'.format(i+1))
        save_image(plate, plate_dir, 'plate.jpg')

        # segmentation
        segments, time = execute_module(Segments.do, plate)
        total_time += time

        # save all segments
        for j, seg in enumerate(segments):
            save_image(seg, plate_dir, 'seg_{:02}.jpg'.format(j+1))
        # end for
    # end for
        
    return total_time
# end function

def save_image(img, *file):
    # gather names
    fname = path.join(*file)
    plate_dir = path.dirname(fname)
    
    if not path.exists(plate_dir):
        os.makedirs(plate_dir)
    # end oif

    if path.exists(fname):
        os.remove(fname)
    # end if

    cv2.imwrite(fname, img)
# end function


def execute_module(method, *args): 
    # get result
    start = cv2.getTickCount()
    result = method(*args)
    time = cv2.getTickCount() - start
    time /= cv2.getTickFrequency()
    return result, time
# end function
