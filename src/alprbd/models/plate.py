"""
Declaration of the Plate class
"""


class Plate:
    """
    Information about detected plate
    """

    def __init__(self, region, image=None):
        """
        Creates new instance of Plate
        :param region: the Region this plate originated from
        """
        self._image = image
        self._region = region   # region this plate belongs to
        self.segments = []      # segments of the plate number
        self.guess = []         # list of (prediction, probability), in descending order

        if image is None:
            self._image = region.image
        # end if
    # end init

    @property
    def image(self):
        """the image of the plate"""
        return self._image
    # end prop

    @property
    def region(self):
        """the image of the plate"""
        return self._region
    # end prop

    @property
    def value(self):
        """returns the top prediction"""
        if len(self.guess) == 0:
            return None
        # end if
        return self.guess[0][0]
    # end prop

# end class
