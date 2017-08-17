"""
Declaration of the Region class
"""


class Region:
    """
    Information about a region of interest
    """

    def __init__(self, image, x, y, height, width):
        """
        Creates new instance of Region
        :param image: Image object this region belongs to
        :param x: start position
        :param y: start position
        :param height: region height
        :param width: region width
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._parent = image

    @property
    def parent(self):
        """gets the Image object this region belongs to"""
        return self._parent

    @property
    def image(self):
        """extract the image of the region"""
        x1, y1 = self.x, self.y
        x2 = self.x + self.height
        y2 = self.y + self.width
        return self._parent.original[x1:x2, y1:y2]

    def bound(self):
        return [self.x, self.y, self.width, self.height]

    @property
    def first_point(self):
        """returns the top-left point of the region"""
        return self.y, self.x

    @property
    def second_point(self):
        """returns the bottom-right point of the region"""
        return self.y + self.width, self.x + self.height

# end class

