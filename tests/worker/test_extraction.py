from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestExtraction(TestCase):
    def test_extraction(self):
        for f in np.sort(os.listdir('samples')):
            #f = '335.jpg'
            file = os.path.join('samples', f)
            frame = alprbd.models.Frame(file)
            frame = alprbd.worker.preprocess.process(frame)
            frame = alprbd.worker.detection.detect_roi(frame)
            frame = alprbd.worker.extraction.extract(frame)

            self.assertIsNotNone(frame.roi)
            if len(frame.plates) == 0:
                print(f, 'has no plates')

            for plate in frame.plates:
                cv2.imshow(f, cv2.resize(plate.image, (320, 150)))
                cv2.waitKey(700)