from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestSegmentation(TestCase):

    def test_segmentation(self):
        return
        for f in np.sort(os.listdir('samples')):
            file = os.path.join('samples', f)
            frame = alprbd.models.Frame(file)
            frame = alprbd.worker.preprocess.process(frame)
            frame = alprbd.worker.detection.detect_roi(frame)
            frame = alprbd.worker.extraction.extract(frame)
            frame = alprbd.worker.segmentation.segment(frame)

            self.assertIsNotNone(frame.roi)

            for plate in frame.plates:
                out = np.zeros((28, 1))
                for seg in plate.segments:
                    self.assertIsNotNone(seg)
                    r, c = seg.shape
                    img = cv2.resize(seg, (28 * c // r, 28))
                    out = np.hstack((out, np.zeros((28, 5)) + 255, img))
                # end for

                r, c = plate.image.shape
                x = out.shape[1]
                org = cv2.resize(plate.image, (x, x * r // c))
                img = np.vstack((org, np.zeros((5, x)) + 255, out))
                cv2.imshow(f, img), cv2.waitKey(800)
            # end for

        # end for
    # end function
# end class
