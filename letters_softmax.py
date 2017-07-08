"""
A very simple DIGIT classifier.
See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
import os
import numpy as np
import tensorflow as tf
from utils import get_letter_data
import config as cfg

# Import data
mnist = get_letter_data()

batch_size = 100
image_dim = 28 * 28
learning_rate = 0.3
num_classes = len(cfg.LETTERS)

# Create the model
X = tf.placeholder(tf.float32, [None, image_dim])
W = tf.Variable(tf.zeros([image_dim, num_classes]))
B = tf.Variable(tf.zeros([num_classes]))
Y = tf.matmul(X, W) + B

# Define loss and optimizer
Y_ = tf.placeholder(tf.float32, [None, num_classes])

# The formulation of cross-entropy
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=Y_, logits=Y))

train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

# Accuracy measure
correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Init session
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

def train_model(i):
    batch_X, batch_Y = mnist.train.next_batch(batch_size)
    sess.run(train_step, feed_dict={X: batch_X, Y_: batch_Y})

    if i % 1000 == 0:
        a, c = sess.run([accuracy, cross_entropy],
                        feed_dict={X: mnist.train.images, Y_: mnist.train.labels})
        print('Train', i, '|', 'accuracy:', a, 'loss:', c)
    # end if
# end function

def main(_):
    # Train
    print()
    for i in range(10000):
        train_model(i)
    # end for

    # Test
    print()
    a, c = sess.run([accuracy, cross_entropy],
                    feed_dict={X: mnist.test.images, Y_: mnist.test.labels})
    print('Test', '|', 'accuracy:', a, 'loss:', c)

    # save trained model
    if not os.path.exists('output'):
        os.makedirs('output')
    # end if
    weight, base = sess.run([W, B])
    np.save(cfg.LETTER_WEIGHTS, weight)
    np.save(cfg.LETTER_BASES, base)
# end function

if __name__ == '__main__':
    tf.app.run(main=main)
# end if
