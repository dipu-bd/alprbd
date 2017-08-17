from unittest import TestCase
import os
import cv2
import alprbd
import numpy as np


class TestDetection(TestCase):
    def test_mixture_model(self):
        q = os.path.abspath('/home/dipu/Desktop/alpr')
        if not os.path.exists(q): os.makedirs(q);
        kernel = alprbd.worker.detection.match_filter()
        self.assertIsNotNone(kernel, msg="mixture model build failure")
        img = 100 * kernel / np.max(kernel) 
        img[img > 255] = 255
        img[img < 0] = 0
        img = np.uint8(img)
        cv2.imwrite(q + '/match-filter.jpg', img)

    def test_apply_matching(self):
        #for f in np.sort(os.listdir('samples')):
        f = '002.jpg'
        file = os.path.join('samples', f)
        image = alprbd.models.Frame(file)
        image = alprbd.worker.preprocess.process(image)
        matched = alprbd.worker.detection.apply_matching(image.enhanced)
        self.assertIsNotNone(matched, msg="mixture model build failure")
        self.assertLessEqual(np.max(matched), 255)
        self.assertGreaterEqual(np.min(matched), 0)
        q = os.path.abspath('/home/dipu/Desktop/alpr')
        if not os.path.exists(q): os.makedirs(q);
        #image.gray[matched < 250] = 0
        #out = np.hstack((image.enhanced, image.gray))
        cv2.imwrite(q + '/gray.jpg', image.gray)
        cv2.imwrite(q + '/enhanced.jpg', image.enhanced)
        cv2.imwrite(q + '/matched.jpg', matched)
        #cv2.imshow(f, out)
        #cv2.waitKey()

    def test_regions(self):
        FALSE = [86,129,41,45,75,106,111,127,130,135,177]
        print('>>FALSE =', len(FALSE))
        p = os.path.abspath('samples')
        #p = os.path.abspath('../alpr-test/LPDB')
        q = os.path.abspath('/home/dipu/Desktop/alpr')
        if not os.path.exists(q): os.makedirs(q);
        i = 0;
        #for f in sorted(os.listdir(p)):
        #n = int(f.split('.')[0])
        #if not n == 1: continue
        f = '002.jpg'
        file = os.path.join(p, f)
        image = alprbd.models.Frame(file)
        image = alprbd.worker.preprocess.process(image)
        image = alprbd.worker.detection.detect_roi(image)
        self.assertIsNotNone(image.roi)
        for region in reversed(image.roi):
            i += 1
            out = os.path.join(q, '{:05d}.jpg'.format(i))
            cv2.imwrite(out, region.image)
            #cv2.imshow(f, cv2.resize(region.image, (300, 120)))
            #cv2.waitKey(600)
