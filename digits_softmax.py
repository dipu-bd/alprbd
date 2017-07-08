"""
Neural network using softmax of topology 784 x 10
"""

import tensorflow as tf
import tensorflowvisu
from utils import get_digit_data

# the dataset
mnist = get_digit_data()

# input X: grayscale images of dimension 28x28=784,
# the first dimension (None) will index the images in the mini-batch
X = tf.placeholder(tf.float32, [None, 784])
# correct answers will go here
Y_ = tf.placeholder(tf.float32, [None, 10])
# weights W[784, 10]   784=28*28
W = tf.Variable(tf.zeros([784, 10]))
# biases b[10]
b = tf.Variable(tf.zeros([10]))

# The model
Ylogits = tf.matmul(X, W) + b
Y = tf.nn.softmax(Ylogits)

# loss function
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
cross_entropy = tf.reduce_mean(cross_entropy) * 100

# accuracy of the trained model, between 0 (worst) and 1 (best)
correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# training, learning rate = 0.005
train_step = tf.train.GradientDescentOptimizer(0.005).minimize(cross_entropy)

# init
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# You can call this function in a loop to train the model, 100 images at a time
def training_step(i, update_test_data, update_train_data):

    # training on batches of 100 images with 100 labels
    batch_X, batch_Y = mnist.train.next_batch(100)

    # compute training values for visualisation
    a, c = sess.run([accuracy, cross_entropy],
                    feed_dict={X: batch_X, Y_: batch_Y})
    print(str(i) + ": accuracy:" + str(a) + " loss: " + str(c))

    # the backpropagation training step
    sess.run(train_step, feed_dict={X: batch_X, Y_: batch_Y})
# end function


# training loop
print('\n')
for i in range(1000):
    training_step(i, False, True)
# end for

# final accuray and error
a, c = sess.run([accuracy, cross_entropy], 
                feed_dict={X: mnist.test.images, Y_: mnist.test.labels})            
print('Final' + ": accuracy:" + str(a) + " loss: " + str(c))
