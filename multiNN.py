# -*- coding: utf-8 -*-
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
          layers,
          iterations=1000,
          batch_size=100,
          model_file=None,
          learning_rate=0.001):
    """
    Builds the model, trains it, and stores the final graph
    """
    tf.set_random_seed(0)

    L = layers
    num_L = len(L)

    # Input
    X = tf.placeholder(tf.float32, [None, L[0]], name='X')
    # Correct output
    Y_ = tf.placeholder(tf.float32, [None, L[-1]], name='Y_')

    # Probability of keeping a node during dropout
    # = 1.0 at test time (no dropout) and 0.75 at training time
    pkeep = tf.placeholder(tf.float32, name='pkeep')

    # Intialize the weights and bases
    B = [None] * (num_L - 1)    # bases
    W = [None] * (num_L - 1)    # weights
    for i in range(num_L - 1):
        # get random numbers between -0.2 and +0.2
        W[i] = tf.Variable(tf.truncated_normal([L[i], L[i + 1]], stddev=0.1))
        # intermediate bases should be ones
        B[i] = tf.Variable(tf.ones([L[i + 1]]))
    # end for
    B[-1] = tf.Variable(tf.zeros([L[-1]]))   # last base is zeros

    # Build the model
    Y = [None] * num_L  # output
    Y[0] = X
    for i in range(num_L - 1):
        # output including dropouts
        Y[i + 1] = tf.nn.dropout(tf.nn.relu(tf.matmul(Y[i], W[i]) + B[i]), pkeep)
    # end for
    Ylogits = tf.matmul(Y[-2], W[-1]) + B[-1]
    YY = Y[-1] = tf.nn.softmax(Ylogits, name='Y')

    # cross-entropy loss function = -sum(Y_i * log(Yi))
    cost = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    # normalised for batches of images
    cost = tf.multiply(tf.reduce_mean(cost), batch_size, name='loss')

    # Defiine optimizer
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    # accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(YY, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Init session
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    print()

    # Training loop
    display_step = 100
    step = 1
    # Keep training until reach max iterations
    output = 'iteration, loss, accuracy\n'
    while step < iterations:
        batch_x, batch_y = ds.train.next_batch(batch_size)
        # Run optimization op (backprop)
        sess.run(optimizer, feed_dict={X: batch_x, Y_: batch_y, pkeep: 0.75})
        # Calculate batch loss and accuracy
        loss, acc = sess.run([cost, accuracy], feed_dict={X: batch_x,
                                                          Y_: batch_y,
                                                          pkeep: 1.})
        if (step <= 50 and step % 10 == 0) or (step % display_step == 0):
            print("Iter " + str(step * batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training Accuracy= " + \
                  "{:.5f}".format(acc))
        # end if
        output += "{}, {:.18f}, {:.18f}\n".format(step * batch_size, loss, acc)
        step += 1
    # end while
    print("\nOptimization Finished!")

    with open(os.path.join('plots', 'digit-all.txt'), 'w') as f:
        f.write(output)
    # end with

    # Calculate accuracy for 256 mnist test images
    print("Testing Accuracy:", \
        sess.run(accuracy, feed_dict={X: ds.test.images,
                                      Y_: ds.test.labels,
                                      pkeep: 1.}))
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
