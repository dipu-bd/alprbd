from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestPreprocess(TestCase):
    def test_process(self):
        file = 'samples/002.jpg'
        image = alprbd.models.Image(file)
        self.assertIsNotNone(image.original, msg="image load failed")
        alprbd.worker.preprocess.process(image)
        self.assertIsNotNone(image.gray, msg="no gray image")
        self.assertEqual(len(image.gray.shape), 2, msg="gray is not 2 dimensional")
        self.assertIsNotNone(image.scaled, msg="scaling failed")
        self.assertEqual(image.scaled.shape[0], alprbd.config.SCALE_DIM[1], msg="scaled height mismatch")
        self.assertEqual(image.scaled.shape[1], alprbd.config.SCALE_DIM[0], msg="scaled width mismatch")
        self.assertIsNotNone(image.enhanced, msg="no enhanced image")

    def test_gray(self):
        file = 'samples/002.jpg'
        img = cv2.imread(file)
        self.assertIsNotNone(img, msg="img load failed")
        gray = alprbd.worker.preprocess.convert_gray(img)
        self.assertIsNotNone(gray, msg="gray conversion failed")
        self.assertEqual(len(gray.shape), 2, msg="gray is not 2 dimensional")

    def test_rescale(self):
        file = 'samples/002.jpg'
        img = cv2.imread(file)
        self.assertIsNotNone(img, msg="img load failed")
        scaled = alprbd.worker.preprocess.rescale(img)
        self.assertIsNotNone(scaled, msg="rescaling failed")
        self.assertEqual(len(scaled.shape), len(img.shape), msg="shape mismatch")
        self.assertEqual(scaled.shape[0], alprbd.config.SCALE_DIM[1], msg="scaled height mismatch")
        self.assertEqual(scaled.shape[1], alprbd.config.SCALE_DIM[0], msg="scaled width mismatch")

    def test_enhance(self):
        file = 'samples/002.jpg'
        img = cv2.imread(file, 0)
        self.assertIsNotNone(img, msg="img load failed")
        img = alprbd.worker.preprocess.rescale(img)
        self.assertIsNotNone(img, msg="img scaling failed")
        out = alprbd.worker.preprocess.enhance(img)
        self.assertIsNotNone(out, msg="enhancement failed")
        self.assertEqual(len(out.shape), len(img.shape), msg="shape mismatch")
