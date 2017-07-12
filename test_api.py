"""
For testing the trained model
"""
import os
from glob import glob
import cv2
import numpy as np
import tensorflow as tf
import config as cfg

def read_images(folder):
    """Read all images from a directory recursively"""
    return np.sort([file for file in glob(folder + '**/*.*', recursive=True)])
# end if

def trim_image(img):
    """Keep only important part"""
    # open
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 2)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 2)
    # crop
    cropped = img[x1:x2, y1:y2]
    # resize
    resized = cv2.resize(cropped, cfg.IMAGE_DIM)
    return resized
# end function

def run(model_file, sample_folder, letters):
    """Main function"""
    # Check sample directory
    if not os.path.exists(sample_folder):
        return print("Samples not found")
    # end if

    # Create session
    sess = tf.Session()
    print()

    # Restore model
    folder = os.path.dirname(model_file)
    saver = tf.train.import_meta_graph(model_file + '.meta')
    saver.restore(sess, tf.train.latest_checkpoint(folder))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name("X:0")
    Y = graph.get_tensor_by_name("Y:0")
    pkeep = graph.get_tensor_by_name("pkeep:0")

    files = read_images(sample_folder)
    for file in files:
        # prepare image data
        image = cv2.imread(file, 0)
        image = trim_image(image)
        image = np.reshape(image, (1, 784))
        # predict outcome
        result = sess.run(Y, {X: image, pkeep: 1.0}).flatten()
        p = np.argmax(result)   # predicted class
        # show result
        name = os.path.split(file)[-1]
        print("%10s = %s (%.2f%% sure)" % (name, letters[p], result[p] * 100))
    # end for

    sess.close()
# end function
