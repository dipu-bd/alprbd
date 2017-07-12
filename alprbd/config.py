"""
Global configuration for ALPR
"""


# Ratio between (red, green, blue) pixels for gray-scale
GRAY_RATIO = (0.59, 0.30, 0.11)

# Default image size for processing
SCALE_DIM = (640, 480)

# plate constraints
MIN_HEIGHT = 30     # in pixels
MIN_WIDTH = 80      # in pixels
MIN_AREA = 0.1      # contour_area / image_area
MIN_ASPECT = 0.3    # contour_height / contour_width
MAX_ASPECT = 0.6    # contour_height / contour_width
MAX_ANGLE = 25      # in degrees

# Default plate size for processing
PLATE_DIM = (500, 250)
