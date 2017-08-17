#!/usr/bin/env python

"""ALPRBD: Automated license plate recognition system for Bangladesh.

ALPRBD provides a api to work with license plate numbers of vehicles 
in Bangladesh. The system is divided into four stages: Detection, 
Extraction, Segmentation, and Recognition.

Detection: locates all possible regions of interest.
Extraction: extracts region of interest and clean them up.
Segmentation: segments characters from license plate.
Recognition: recognizes each segments with a probability.

Finally all modules put together to display the final results
of recognized plate numbers with their accuracy in percentage.
"""
from setuptools import setup

DOCLINES = (__doc__ or '').split("\n")

setup(
    name='alprbd',
    version='1.0',
    description='Automated License Plate Recognition for Bangladesh',
    url='http://github.com/dipu-bd/alprbd',
    author='Sudipto Chandra',
    author_email='dipu.sudipta@gmail.com',
    license='MIT',
    packages=[
        'alprbd'
    ],
    zip_safe=False
)
