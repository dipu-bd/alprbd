"""
A very simple DIGIT classifier.
See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
import sys
import tensorflow as tf
from utils import get_digit_data

# Import data
mnist = get_digit_data()

# Create the model
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])

# The formulation of cross-entropy
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Accuracy measure
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Init session
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

def train_model():
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
# end function

def test_model(msg):
    a, c = sess.run([accuracy, cross_entropy],
                    feed_dict={x: mnist.test.images, y_: mnist.test.labels})
    print(msg, 'accuracy:', a, 'loss:', c)
# end function

def main(_):
    print('\n')

    # Train
    for i in range(10000):
        train_model()
        if i % 1000 == 0:
            test_model(str(i) + " |")
        # end if
    # end for

    # Test trained model
    test_model("\nFinal |")
# end main

if __name__ == '__main__':
    tf.app.run(main=main)
# end if
