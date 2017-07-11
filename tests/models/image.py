from unittest import TestCase
import alprbd
import logging


class TestImage(TestCase):
    def test_init(self):
        file = 'samples/002.jpg'
        img = alprbd.models.Image(file)
        self.assertIsNotNone(img.file, msg="no file given")
        logging.info('>>>image test: file ' + img.file)
        self.assertIsNotNone(img.original, msg="image load failure")
        logging.info('>>>image test: file ' + str(img.original.shape))
        self.assertEqual(len(img.original.shape), 3, msg="not a color image")
        self.assertEqual(img.original.shape[2], 3, msg="not 3 color image")
        self.assertEqual(img.height, 2448, msg="height mismatch")
        self.assertEqual(img.width, 3264, msg="width mismatch")
        self.assertEqual(len(img.roi), 0, msg="error: region of interest array")
        self.assertEqual(len(img.plates), 0, msg="error: plate array")
        img.save()

