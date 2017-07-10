"""
Declaration of the Segment class
"""


class Segment:
    """
    Single segment of plate number
    """

    def __init__(self, id):
        self._id = id       # segment id
        self.guess = []     # list of (prediction, probability), in descending order

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        """returns the top predicted value"""
        return self.guess[0][0]

# end class
