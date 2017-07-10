"""
Declaration of the Segment class
"""


class Segment:
    """
    Single segment of plate number
    """

    def __init__(self, plate, id):
        self._id = id           # segment id
        self._plate = plate     # plate
        self.guess = []         # list of (prediction, probability), in descending order

    @property
    def id(self):
        """id of the segment"""
        return self._id

    @property
    def value(self):
        """returns the top predicted value"""
        if len(self.guess) == 0:
            return None
        return self.guess[0][0]

    @property
    def plate(self):
        """get the plate which this segment belongs to"""
        return self._plate

# end class
