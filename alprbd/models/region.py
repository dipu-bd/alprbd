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
        self._x1 = x
        self._x2 = x + height
        self._y1 = y
        self._y2 = y + width
        self._parent = image

    @property
    def image(self):
        """extract the image of the region"""
        return self._parent.original[self._x1:self._x2, self._y1:self._y2]

    @property
    def width(self):
        """get width of the region"""
        return self._y2 - self._y1

    @property
    def height(self):
        """get height of the region"""
        return self._x2 - self._x1

# end class
