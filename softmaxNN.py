"""
5 layer Neural network classifier using softmax activation.
"""
import os
import math
import numpy as np
import tensorflow as tf

def train(ds,
          layers,
          iterations=10000,
          batch_size=100,
          model_file=None):
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

    # Decaying learning rate
    lr = tf.placeholder(tf.float32)

    # Probability of keeping a node during dropout
    # = 1.0 at test time (no dropout) and 0.75 at training time
    pkeep = tf.placeholder(tf.float32, name='pkeep')

    # Intialize the weights and bases
    B = [None] * num_L  # bases
    W = [None] * num_L  # weights
    for i in range(1, num_L):
        # get random numbers between -0.2 and +0.2
        W[i] = tf.Variable(tf.truncated_normal([L[i - 1], L[i]], stddev=0.1))
        # intermediate bases should be ones
        B[i] = tf.Variable(tf.ones([L[i]]))
    # end for
    B[-1] = tf.Variable(tf.zeros([L[i]]))   # last base is zeros

    # Connect the layers
    Y = [None] * num_L  # output
    Y[0] = X
    for i in range(1, num_L - 1):
        # output including dropouts
        Y[i] = tf.nn.dropout(tf.nn.relu(tf.matmul(Y[i - 1], W[i]) + B[i]), pkeep)
    # end for
    Ylogits = tf.matmul(Y[-2], W[-1]) + B[-1]
    YY = Y[-1] = tf.nn.softmax(Ylogits, name='Y')

    # cross-entropy loss function = -sum(Y_i * log(Yi))
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    # normalised for batches of images
    cross_entropy = tf.multiply(tf.reduce_mean(cross_entropy), batch_size, name='loss')

    # accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(YY, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Defiine optimizer
    train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

    # Accuracy measures
    correct_prediction = tf.equal(tf.argmax(YY, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    # Init session
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    print()

    # Training loop
    log_amount = 25
    pitstop = 1 + (iterations // log_amount)
    iterations = pitstop * log_amount
    max_lr = 0.003
    min_lr = 0.0001
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
            print("step %5d | accuracy = %6.2f%% | loss = %8.3f | LR = %f"
                  % (i, a * 100, c, learning_rate))
        # end if
    # end for
    print('Training Complete.')
    print()

    # Save the model
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
# end function
