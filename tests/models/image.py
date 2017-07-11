from unittest import TestCase
import alprbd


class TestImage(TestCase):
    def test_all(self):
        img = alprbd.models.Image('../samples/002.jpg')
        assert img.file is not None
        assert img.image.shape[2] == 3
        assert img.height == 2448
        assert img.width == 3264
        assert img.gray is None
        assert len(img.roi) == 0
        assert len(img.plates) == 0
        img.save()
