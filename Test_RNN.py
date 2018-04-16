from __future__ import print_function, division
import os
import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn

"""GENERATE DATA"""
input_size = 3                                                          # Max size of inputs
hidden_size = 10                                                        # Size of the hidden layers
output_size = 3                                                         # Max size of outputs
"""INITIALIZE NETWORK"""

x = tf.placeholder(tf.float32, [None, 1, input_size])                   # Inputs
y = tf.placeholder(tf.float32, [1, output_size])                        # Desired Outputs

weights = tf.Variable(tf.random_normal([hidden_size, output_size]))     # Create weights between the hidden layer and output
biases = tf.Variable(tf.random_normal([output_size]))                   # Create biases for Output layer

lstm_cell = rnn.BasicLSTMCell(hidden_size, forget_bias=1.0)             # Create a LSTM cell

outputs, state = tf.nn.dynamic_rnn(lstm_cell, x, dtype=tf.float32,      # Create the outputs from LSTM
                                   time_major=True)

prediction_operation = tf.matmul(outputs[-1], weights) + biases         # prediction Operation

loss_operation = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=prediction_operation, labels=y))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)

train_operation = optimizer.minimize(loss_operation)

sess = tf.Session()

sess.run(tf.initialize_all_variables())

_x = [[[1, 2, 3]]]

_y = [[2, 4, 6]]

for idx in range(200):
    result = sess.run(train_operation,
                      feed_dict={
                          x: _x,
                          y: _y
                      })

pred = sess.run(prediction_operation,
                feed_dict={
                    x: _x
                })

print(pred)
"""TRAINING"""