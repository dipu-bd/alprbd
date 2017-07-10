"""
Declaration of the Plate class
"""


class Plate:
    """
    Information about detected plate
    """

    def __init__(self, region):
        """
        Creates new instance of Plate
        :param region: the Region this plate originated from
        """
        self._region = region   # region this plate belongs to
        self.segments = []      # segments of the plate number
        self.guess = []         # list of (prediction, probability), in descending order

    @property
    def plate_image(self):
        """the image of the plate"""
        return self._region.image()

    @property
    def value(self):
        """returns the top prediction"""
        if len(self.guess) == 0:
            return None
        return self.guess[0][0]

# end class
