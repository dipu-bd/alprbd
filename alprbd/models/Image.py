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
        self._file = os.path.abspath(image_file)
        self._image = cv2.imread(self._file)
    # end function

    @property
    def file(self):
        """image file path"""
        return self._file

    @property
    def image(self):
        """original image"""
        return self._image

    @property
    def gray_image(self):
        """image converted to grayscale"""
        return self['_gray']

    def save(self):
        """Saves the image to the file"""
        cv2.imwrite(self._file, self._image)

# end class


img = Image("test.jpg")

