"""
5 layer Neural network classifier using softmax activation.
"""
import os
import math
import numpy as np
import tensorflow as tf
import config as cfg
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def train(ds,
          image_size,
          num_classes,
          iterations=1000,
          batch_size=100,
          model_file=None,
          max_learning_rate=0.003,
          min_learning_rate=0.0001):
    """
    Builds the model, trains it, and stores the final graph
    """
    tf.set_random_seed(0)

    # input X: 28x28 grayscale images, the first dimension (None) will index the images in the mini-batch
    height, width = image_size
    X = tf.placeholder(tf.float32, [None, height, width, 1])
    # correct answers will go here
    Y_ = tf.placeholder(tf.float32, [None, num_classes])
    # variable learning rate
    lr = tf.placeholder(tf.float32)

    # three convolutional layers with their channel counts, and a
    # fully connected layer (tha last layer has 10 softmax neurons)
    K = 4  # first convolutional layer output depth
    L = 8  # second convolutional layer output depth
    M = 12  # third convolutional layer
    N = 200  # fully connected layer

    W1 = tf.Variable(tf.truncated_normal([5, 5, 1, K], stddev=0.1))  # 5x5 patch, 1 input channel, K output channels
    B1 = tf.Variable(tf.ones([K])/10)
    W2 = tf.Variable(tf.truncated_normal([5, 5, K, L], stddev=0.1))
    B2 = tf.Variable(tf.ones([L])/10)
    W3 = tf.Variable(tf.truncated_normal([4, 4, L, M], stddev=0.1))
    B3 = tf.Variable(tf.ones([M])/10)

    W4 = tf.Variable(tf.truncated_normal([4 * 7 * 7 * M, N], stddev=0.1))
    B4 = tf.Variable(tf.ones([N])/10)
    W5 = tf.Variable(tf.truncated_normal([N, num_classes], stddev=0.1))
    B5 = tf.Variable(tf.ones([num_classes])/10)

    # Probability of keeping a node during dropout
    # = 1.0 at test time (no dropout) and 0.75 at training time
    pkeep = tf.placeholder(tf.float32, name='pkeep')

    # The model
    stride = 1  # output is 28x28
    Y1 = tf.nn.relu(tf.nn.conv2d(X, W1, strides=[1, stride, stride, 1], padding='SAME') + B1)
    stride = 2  # output is 14x14
    Y2 = tf.nn.relu(tf.nn.conv2d(Y1, W2, strides=[1, stride, stride, 1], padding='SAME') + B2)
    stride = 2  # output is 7x7
    Y3 = tf.nn.relu(tf.nn.conv2d(Y2, W3, strides=[1, stride, stride, 1], padding='SAME') + B3)

    # reshape the output from the third convolution for the fully connected layer
    YY = tf.reshape(Y3, shape=[-1, 4 * 7 * 7 * M])

    Y4 = tf.nn.relu(tf.matmul(YY, W4) + B4)
    Ylogits = tf.matmul(Y4, W5) + B5
    Y = tf.nn.softmax(Ylogits)

    # The softmax_cross_entropy_with_logits function to avoid numerical stability
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    cross_entropy = tf.reduce_mean(cross_entropy)*100

    # Accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Training step, the learning rate is a placeholder
    train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

    # Init session
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    print()

    # Training loop
    log_amount = 25
    pitstop = 1 + (iterations // log_amount)
    iterations = pitstop * log_amount
    max_lr = max_learning_rate
    min_lr = min_learning_rate
    decay_speed = iterations
    for i in range(1, iterations + 1):
        # learning rate decay
        learning_rate = min_lr + (max_lr - min_lr) * math.exp(-i / decay_speed)

        # training step
        batch_X, batch_Y = ds.train.next_batch(batch_size)
        sess.run(train_step, {X: batch_X, Y_: batch_Y, lr: learning_rate, pkeep: 0.75})

        # print at each pitstop
        if i % pitstop == 0:
            feed_dict = {X: ds.test.images, Y_: ds.test.labels, pkeep: 1.0}
            a, c = sess.run([accuracy, cross_entropy], feed_dict)
            out_str = "step %5d | accuracy = %6.2f%% | loss = %8.3f | LR = %f"
            print(out_str % (i, a * 100, c, learning_rate))
        # end if
    # end for
    print('Training Complete.')
    print()

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

    # Save the model normally
    if model_file:
        folder = os.path.dirname(model_file)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # end if
        w, b = sess.run([W, B])
        np.savez_compressed(model_file, weights=w, bases=b)
    # end if

    sess.close()
# end function
