# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def calculate(img):
    """
    Calculate the horizontal projections.
    :param img: plate image 
    """


# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Converts to black and white")
    for read in util.get_images(prev):
        # get plate from last stage
        plate = util.stage_image(read, prev)
        plate = cv2.imread(plate, cv2.CV_8UC1)

        # get result
        segments, time = util.execute_module(calculate, plate)
        runtime.append(time)

        # save all segments
        for idx, seg in enumerate(segments):
            name = "{}.{}".format(idx, read)
            write = util.stage_image(name, cur)
            cv2.imwrite(write, seg)
        # end for

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
