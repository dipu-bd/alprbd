import numpy from np
from alprbd.models.image import Image

img = Image('samples/002.jpg')


def file():
    assert img.file == 'samples/002.jpg'


def image():
    assert np.array(img.image).shape[3] == 3


def save():
    img.save()

