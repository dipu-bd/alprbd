from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestRecognition(TestCase):

    def test_recognition(self):
        for f in np.sort(os.listdir('samples')):
            file = os.path.join('samples', f)
            frame = alprbd.models.Frame(file)
            frame = alprbd.worker.preprocess.process(frame)
            frame = alprbd.worker.detection.detect_roi(frame)
            frame = alprbd.worker.extraction.extract(frame)
            frame = alprbd.worker.segments.segment(frame)
            frame = alprbd.worker.recognize.recognize(frame)

            for plate in frame.plates:
                if len(plate.guess) > 0:
                    print(f, plate.value, plate.guess[0][1])
            # end for

        # end for
    # end function
# end class
