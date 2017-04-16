# -*- coding: utf-8 -*-

import os
from os import path

import Segments
from Extraction import extract


def execute(file):
    """
    Execute the ALPR process
    :param stage: Stage number
    """ 
    save_dir = path.dirname(file)
    img = cv2.imread(file)
    total_time = 0

    # execute extraction
    print("Extracting all plate like regions...")
    plates, time = execute_module(extract, img)
    total_time += time

    for i, plate in enumerate(plates):
        plate_dir = path.join(save_dir, 'plates', str(i))
        os.mkdirs(plate_dir)

        # save plate
        fname = path.join(plate_dir, 'plate.jpg')
        cv2.imwrite(fname, plate)

        # segmentation
        segments, time = execute_module(Segments.do, plate)
        total_time += time

        # save all segments
        for j, seg in enumerate(segments):
            fname = path.join(plate_dir, 'seg'+ str(j) + '.jpg')
            cv2.imwrite(fname, seg)
        # end for
    # end for

    return total_time
# end function


def execute_module(method, *args): 
    # get result
    start = cv2.getTickCount()
    result = method(*args)
    time = cv2.getTickCount() - start
    time /= cv2.getTickFrequency()
    return result, time
# end function
