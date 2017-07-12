from unittest import TestCase
import os
import random
import cv2
import alprbd
import numpy as np


class TestExtraction(TestCase):

    def test_extraction(self):
        return None
        for f in np.sort(os.listdir('samples')):
            #f = '335.jpg'
            file = os.path.join('samples', f)
            frame = alprbd.models.Frame(file)
            frame = alprbd.worker.preprocess.process(frame)
            frame = alprbd.worker.detection.detect_roi(frame)
            frame = alprbd.worker.extraction.extract(frame)

            self.assertIsNotNone(frame.roi)

            img = frame.original
            for plate in frame.plates:
                color = [255, 0, random.randint(0, 127)]
                random.shuffle(color)
                cv2.putText(img, f, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], thickness=10)
                img[:480, :180] = 255
                cv2.rectangle(img,
                              plate.region.first_point,
                              plate.region.second_point,
                              color, thickness=20)
            # end for
            cv2.imshow("marked", alprbd.worker.preprocess.rescale(img, (800, 600)))
            for plate in frame.plates:
                cv2.imshow('plate', plate.image)
                cv2.waitKey(2000)
