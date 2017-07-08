"""
1 layer Neural network classifier using softmax activation.
"""
import os
import numpy as np
import tensorflow as tf

def train(ds,
          base_file,
          weights_file,
          layers,
          learning_rate=0.3,
          iterations=10000,
          batch_size=100):
    """
    Initialize the model, train the network, and store output
    """
    # Input
    X = tf.placeholder(tf.float32, [None, layers[0]])
    # Correct output
    Y_ = tf.placeholder(tf.float32, [None, layers[-1]])

    # Build the model
    num_layers = len(layers)
    B = [None] * num_layers  # bases
    W = [None] * num_layers  # weights
    Y = [None] * num_layers  # output

    Y[0] = X
    for i in range(1, num_layers)
        # get random numbers between -0.2 and +0.2
        W[i] = tf.Variable(tf.truncated_normal([layers[i-1], layers[i]], stddev=0.1))
        B[i] = tf.Variable(tf.zeros([layers[i]]))
        Y[i] = tf.nn.sigmoid(tf.matmul(Y[i-1], W[i]) + B[i])
    # end for
    
    Ylogits = tf.matmul(Y[-2], W[-1]) + B[-1]
    YY = Y[-1] = tf.nn.softmax(Ylogits)
    
    # cross-entropy loss function = -sum(Y_i * log(Yi))
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    # normalised for batches of images
    cross_entropy = tf.reduce_mean(cross_entropy) * batch_size

    # accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(YY, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Defiine optimizer
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

    # Accuracy measures
    correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Init session
    init = tf.global_variables_initializer()
    sess = tf.InteractiveSession()
    sess.run(init)
    print()

    # Training loop
    pitstop = iterations // 25
    for i in range(iterations):
        batch_X, batch_Y = ds.train.next_batch(batch_size)
        sess.run(train_step, {X: batch_X, Y_: batch_Y})
        
        if i % pitstop == 0:
            a, c = sess.run([accuracy, cross_entropy],
                            {X: ds.train.images, Y_: ds.train.labels})
            print('step', i, '|', 'accuracy:', a, 'loss:', c)
        # end if
    # end for
    print()

    # Test accuracy
    a, c = sess.run([accuracy, cross_entropy],
                    {X: ds.test.images, Y_: ds.test.labels})
    print('Training Complete.', '|', 'Accuracy:', a, 'Loss:', c)
    print()

    # Save the model
    base, weight = sess.run([B, W])
    np.save(base_file, base)
    np.save(weights_file, weight)
    print('Training result stored.\n')    
# end function
