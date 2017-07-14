"""
For testing the trained model
"""
import os
from glob import glob
import cv2
import numpy as np
import tensorflow as tf
import config as cfg
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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

    # Build model
    model = np.load(model_file)

    files = read_images(sample_folder)
    for file in files:
        # prepare image data
        image = cv2.imread(file, 0)
        image = trim_image(image)
        image = np.reshape(image, (1, 784))
        # predict outcome
        result = predict(model, image).flatten()
        p = np.argmax(result)           # predicted class
        # show result
        name = os.path.split(file)[-1]
        print("%10s = %s (%.2f%% sure)" % (name, letters[p], result[p] * 100))
    # end for
# end function

def predict(model, input):
    """predicts outcome of the given input"""
    W = model['weights']
    B = model['bases']
    num = W.shape[0]

    X = tf.placeholder(tf.float32)
    for i in range(num):
        W[i] = tf.Variable(W[i], tf.float32)
        B[i] = tf.Variable(B[i], tf.float32)

    # for each inner layers
    Y = X
    for i in range(0, num - 1):
        Y = tf.nn.relu(tf.matmul(Y, W[i]) + B[i])

    # for the final layer
    Y = tf.nn.softmax(tf.matmul(Y, W[-1]) + B[-1])
    
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        return sess.run(Y, { X: input })
# end function
