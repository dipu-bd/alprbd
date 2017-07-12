from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestDetection(TestCase):
    def test_mixture_model(self):
        kernel = alprbd.worker.detection.match_filter()
        self.assertIsNotNone(kernel, msg="mixture model build failure")
        #cv2.imshow('kernel: ', cv2.resize(kernel, (400, 150)))
        #cv2.waitKey(5000)

    def test_apply_matching(self):
        #for f in np.sort(os.listdir('samples')):
        f = '337.jpg'
        file = os.path.join('samples', f)
        image = alprbd.models.Frame(file)
        image = alprbd.worker.preprocess.process(image)
        matched = alprbd.worker.detection.apply_matching(image.enhanced)
        self.assertIsNotNone(matched, msg="mixture model build failure")
        self.assertLessEqual(np.max(matched), 255)
        self.assertGreaterEqual(np.min(matched), 0)
        image.gray[matched < 250] = 0
        out = np.hstack((image.enhanced, image.gray))
        cv2.imshow('matched: ' + f, out)
        cv2.waitKey()

    def test_regions(self):
        for f in np.sort(os.listdir('samples')):
            #f = '335.jpg'
            file = os.path.join('samples', f)
            image = alprbd.models.Frame(file)
            image = alprbd.worker.preprocess.process(image)
            image = alprbd.worker.detection.detect_roi(image)
            for region in reversed(image.roi):
                cv2.imshow(f, cv2.resize(region.image, (350, 150)))
                cv2.waitKey(700)