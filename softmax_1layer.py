"""
1 layer Neural network classifier using softmax activation.
"""
import os
import numpy as np
import tensorflow as tf

def train(ds,
          base_file,
          weights_file,
          input_dim,
          output_dim,
          learning_rate=0.3,
          iterations=10000,
          batch_size=100):
    """
    Trains
    """
    # Create the model
    X = tf.placeholder(tf.float32, [None, input_dim])
    W = tf.Variable(tf.zeros([input_dim, output_dim]))
    B = tf.Variable(tf.zeros([output_dim]))
    Y = tf.matmul(X, W) + B

    # Original output
    Y_ = tf.placeholder(tf.float32, [None, output_dim])

    # Define loss / cross_entropy
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=Y_, logits=Y))

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
        sess.run(train_step, feed_dict={X: batch_X, Y_: batch_Y})

        if i % pitstop == 0:
            a, c = sess.run([accuracy, cross_entropy],
                            feed_dict={X: ds.train.images, Y_: ds.train.labels})
            print('step', i, '|', 'accuracy:', a, 'loss:', c)
        # end if
    # end for
    print()

    # Test results
    a, c = sess.run([accuracy, cross_entropy],
                    feed_dict={X: ds.test.images, Y_: ds.test.labels})
    print('Training Complete.', '|', 'Accuracy:', a, 'Loss:', c)
    print()

    # Save the model
    base, weight = sess.run([B, W])
    np.save(base_file, base)
    np.save(weights_file, weight)
    print('Training result stored.\n')    
# end function
