from unittest import TestCase
import alprbd


class TestImage(TestCase):
    def test_all(self, file='samples/002.jpg'):
        img = alprbd.models.Image(file)
        assert img.file is not None
        assert img.original.shape[2] == 3
        assert img.height == 2448
        assert img.width == 3264
        assert len(img.roi) == 0
        assert len(img.plates) == 0
        img.save()
