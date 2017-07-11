"""
Contains declaration of Image class.
Image object is used everywhere for recognition process.
"""

import os
import cv2


class Image:
    """
    Image object that is used for recognition process.
    """

    def __init__(self, image_file):
        """
        Creates a new instance of Image
        :param image_file: image file path
        """
        self._file = os.path.abspath(image_file)    # private variable
        self.original = cv2.imread(self._file)      # original image
        self.roi = []                               # regions of interest
        self.plates = []                            # all detected plates
    # end function

    @property
    def file(self):
        """image file path"""
        return self._file

    @property
    def height(self):
        """height of the image"""
        return self.original.shape[0]

    @property
    def width(self):
        """width of the image"""
        return self.original.shape[1]

    def save(self):
        """saves the image to the file"""
        cv2.imwrite(self._file, self.original)

# end class
