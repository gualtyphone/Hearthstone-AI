from __future__ import print_function, division
import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import BoardState
import numpy as np
import GameLoader
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class RNN(object):
    def __init__(self):
        """ TODO: Implement Constructor """
        # Variables
        self.num_epochs = 100
        self.total_series_length = 50000
        self.truncated_backprop_length = 15
        self.state_size = 4
        self.num_classes = 2
        self.echo_step = 3
        self.batch_size = 5
        self.num_batches = self.total_series_length // self.batch_size // self.truncated_backprop_length
        self.num_layers = 3

        self.RUN_NAME = "Run 20"

        # Tesnorflow placeholders
        self.batchX_placeholder = tf.placeholder(tf.float32, [self.batch_size, self.truncated_backprop_length])
        self.batchY_placeholder = tf.placeholder(tf.int32, [self.batch_size, self.truncated_backprop_length])

        self.init_state = tf.placeholder(tf.float32, [self.num_layers, 2, self.batch_size, self.state_size])

        self.state_per_layer_list = tf.unstack(self.init_state, axis=0)
        self.rnn_tuple_state = tuple(
            [tf.nn.rnn_cell.LSTMStateTuple(self.state_per_layer_list[idx][0], self.state_per_layer_list[idx][1])
             for idx in range(self.num_layers)]
        )

        # Weights
        self.W2 = tf.Variable(np.random.rand(self.state_size, self.num_classes), dtype=tf.float32)

        # Biases
        self.b2 = tf.Variable(np.zeros((1, self.num_classes)), dtype=tf.float32)

        def get_a_cell(lstm_size, keep_prob):
            lstm = tf.nn.rnn_cell.BasicLSTMCell(lstm_size, state_is_tuple=True)
            drop = tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=keep_prob)
            return drop

        self.cell = tf.nn.rnn_cell.MultiRNNCell(
            [get_a_cell(self.state_size, 0.5) for _ in range(self.num_layers)], state_is_tuple=True
        )

        self.states_series, self.current_state = tf.nn.dynamic_rnn(self.cell, tf.expand_dims(self.batchX_placeholder, -1),
                                                                   initial_state=self.rnn_tuple_state)
        self.states_series = tf.reshape(self.states_series, [-1, self.state_size])

        self.logits = tf.matmul(self.states_series, self.W2) + self.b2  # Broadcasted addition
        self.labels = tf.reshape(self.batchY_placeholder, [-1])

        # Calculating Loss
        self.logits_series = tf.unstack(
            tf.reshape(self.logits, [self.batch_size, self.truncated_backprop_length, self.num_classes]), axis=1)
        self.predictions_series = [tf.nn.softmax(logit) for logit in self.logits_series]

        self.losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.logits, labels=self.labels)
        self.total_loss = tf.reduce_mean(self.losses)

        self.train_step = tf.train.AdagradOptimizer(0.3).minimize(self.total_loss)

        """ INITIALIZE TENSORFLOW SESSION """
        self.sess = tf.Session()

        self.sess.run(tf.initialize_all_variables())
        self.loss_list = []

    def generateData(self):
        """ TODO: Implement Data Generation"""
        # This will get the data from the boardState and return it in a readable way by the LSTM network
        x = np.array(np.random.choice(2, self.total_series_length, p=[0.5, 0.5]))
        y = np.roll(x, self.echo_step)
        y[0:self.echo_step] = 0

        x = x.reshape((self.batch_size, -1))  # The first index changing slowest, subseries as rows
        y = y.reshape((self.batch_size, -1))

        return (x, y)

    def train(self):
        """ TODO: Implement """
        # Takes the Boardstate with possible choices and returns the predicted move,
        # saving the error and updates the network
        x, y = self.generateData()
        _current_state = np.zeros((self.num_layers, 2, self.batch_size, self.state_size))

        # print("New data, Epoch", self.epoch_idx)

        for batch_idx in range(self.num_batches):
            start_idx = batch_idx * self.truncated_backprop_length
            end_idx = start_idx + self.truncated_backprop_length

            batchX = x[:, start_idx:end_idx]
            batchY = y[:, start_idx:end_idx]

            _total_loss, _train_step, _current_state, _prediction_series = self.sess.run(
                [self.total_loss, self.train_step, self.current_state, self.predictions_series],
                feed_dict={
                    self.batchX_placeholder: batchX,
                    self.batchY_placeholder: batchY,
                    self.init_state: _current_state
                })

            self.loss_list.append(_total_loss)

            if batch_idx % 100 == 0:
                print("Step", batch_idx, "Loss", _total_loss)
                self.plot(self.loss_list, _prediction_series, batchX, batchY)

    def test(self):
        """ TODO: Implement """
        # Takes the Boardstate with possible choices and returns the predicted move,
        # saving the error but not updating the network

    def predict(self):
        """ TODO: Implement """
        # Takes the Boardstate with possible choices and returns the predicted move

    def plot(self, loss_list, predictions_series, batchX, batchY):
        """ TODO: Implement Plotting """
        # Using the plotting tools we can create graphs to represent the network working

