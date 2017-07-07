"""
Formats images to feed into tensorflow
"""
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from glob import glob

FOLDER = './output/generated'


def read_images():
    files = [file for file in glob(FOLDER + '/**/*.bmp', recursive=True)]
    print(len(files))
# end if

read_images()
