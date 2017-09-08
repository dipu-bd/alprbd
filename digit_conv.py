# -*- coding: utf-8 -*-
"""
5 layer Neural network classifier using softmax activation.
"""
import os
import cv2
import math
import numpy as np
from glob import glob
import tensorflow as tf
import config as cfg
from utils import get_digit_data
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.set_random_seed(0)

mnist = get_digit_data()

# Parameters
learning_rate = 0.001
training_iters = 100000
batch_size = 100
display_step = 100

# Network Parameters
n_input = 784 # MNIST data input (img shape: 28*28)
n_classes = len(cfg.NUMERALS) # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)


# Create some wrappers for simplicity
def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME')


# Create model
def conv_net(x, weights, biases, dropout):
    # Reshape input picture
    x = tf.reshape(x, shape=[-1, 28, 28, 1])

    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Max Pooling (down-sampling)
    conv1 = maxpool2d(conv1, k=2)

    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Max Pooling (down-sampling)
    conv2 = maxpool2d(conv2, k=2)

    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tf.nn.dropout(fc1, dropout)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Store layers weight & bias
weights = {
    # 5x5 conv, 1 input, 32 outputs
    'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
    # 5x5 conv, 32 inputs, 64 outputs
    'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
    # fully connected, 7*7*64 inputs, 1024 outputs
    'wd1': tf.Variable(tf.random_normal([7*7*64, 1024])),
    # 1024 inputs, 10 outputs (class prediction)
    'out': tf.Variable(tf.random_normal([1024, n_classes]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([32])),
    'bc2': tf.Variable(tf.random_normal([64])),
    'bd1': tf.Variable(tf.random_normal([1024])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = conv_net(x, weights, biases, keep_prob)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    step = 1
    # Keep training until reach max iterations
    output = "iteration, loss, accuracy\n"
    while step * batch_size < training_iters:
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        # Run optimization op (backprop)
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y,
                                       keep_prob: dropout})
        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,
                                                            y: batch_y,
                                                            keep_prob: 1.})
        if (step <= 50 and step % 10 == 0) or (step % display_step == 0):
            # Calculate batch loss and accuracy
            print("Iter " + str(step * batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training Accuracy= " + \
                  "{:.5f}".format(acc))
        # end if
        output += "{}, {:.18f}, {:.18f}\n".format(step * batch_size, loss, acc)
        step += 1
    # end while
    print("Optimization Finished!")

    with open(os.path.join('plots', 'digits-cnn.txt'), 'w') as f:
        f.write(output)
    # end with

    # Calculate accuracy for 256 mnist test images
    print("Testing Accuracy:", \
        sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y: mnist.test.labels,
                                      keep_prob: 1.}))

    # Save the model using saver
    """
    if model_file:
        folder = os.path.dirname(model_file)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # end if

        # Create saver
        saver = tf.train.Saver()
        saver.save(sess, model_file)
        print('Training model stored.\n')
    # end if
    """

    def read_images(folder):
        """Read all images from a directory recursively"""
        return sorted([file for file in glob(os.path.join(folder, '**', '*.*'), recursive=True)])
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

    # test letters
    letters = cfg.NUMERALS
    for file in read_images(cfg.DIGIT_SAMPLES):
        # prepare image data
        image = cv2.imread(file, 0)
        image = trim_image(image)
        image = np.reshape(image, (1, 784))
        # predict outcome
        result = sess.run(tf.nn.softmax(pred), feed_dict={x: image, keep_prob: 1.})
        result = result.flatten()
        p = np.argmax(result)           # predicted class
        # show result
        name = os.path.split(file)[-1]
        print("%10s = %s (%.2f%% sure)" % (name, letters[p], result[p] * 100))
    # end for


# Iter 1000, Minibatch Loss= 2699463.000000, Training Accuracy= 0.66000
# Iter 2000, Minibatch Loss= 284226.906250, Training Accuracy= 0.94000
# Iter 3000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 4000, Minibatch Loss= 7335.979980, Training Accuracy= 0.99000
# Iter 5000, Minibatch Loss= 28762.919922, Training Accuracy= 0.99000
# Iter 10000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 20000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 30000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 40000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 50000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 60000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 70000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 80000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Iter 90000, Minibatch Loss= 0.000000, Training Accuracy= 1.00000
# Optimization Finished!
# Testing Accuracy: 1.0
#      0.jpg = ০ (100.00% sure)
#    1_1.jpg = ১ (100.00% sure)
#    1_2.jpg = ১ (100.00% sure)
#    1_3.jpg = ১ (100.00% sure)
#    1_4.jpg = ১ (100.00% sure)
#      2.jpg = ২ (100.00% sure)
#    3_1.jpg = ৩ (100.00% sure)
#    3_2.jpg = ৩ (100.00% sure)
#      4.jpg = ৪ (100.00% sure)
#      5.jpg = ৫ (100.00% sure)
#      6.jpg = ৬ (100.00% sure)
#    7_1.jpg = ৭ (100.00% sure)
#    7_2.jpg = ৭ (100.00% sure)
#      8.jpg = ৮ (100.00% sure)
#    8_2.jpg = ৮ (100.00% sure)
#      9.jpg = ৯ (100.00% sure)
#    9_1.jpg = ৯ (100.00% sure)
