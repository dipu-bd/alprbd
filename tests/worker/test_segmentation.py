from unittest import TestCase
import os
import random
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
            self.assertNotEqual(len(frame.plates), 0)

            img = frame.original
            for plate in frame.plates:
                color = [255, 0, random.randint(0, 127)]
                random.shuffle(color)
                img[:180, :460, ] = 255
                cv2.putText(img, f, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], thickness=10)
                cv2.rectangle(img,
                              plate.region.first_point,
                              plate.region.second_point,
                              color, thickness=20)
            # end for
            cv2.imshow("plates", alprbd.worker.preprocess.rescale(img))
            cv2.waitKey(2000)
