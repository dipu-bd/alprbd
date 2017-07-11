from unittest import TestCase
import cv2
import alprbd


class TestImage(TestCase):
    def test_all(self):
        file = 'samples/002.jpg'
        image = alprbd.models.Image(file)
        alprbd.worker.preprocess.process(image)
        assert image.gray is not None
        assert len(image.gray.shape) == 2
        assert image.scaled is not None
        assert image.scaled.shape[0] == alprbd.config.SCALE_DIM[1]
        assert image.scaled.shape[1] == alprbd.config.SCALE_DIM[0]
        cv2.imshow("Original Image", image.original)
        cv2.imshow("Gray Image", image.gray)
        cv2.imshow("Scaled Image", image.scaled)
        cv2.waitKey()

