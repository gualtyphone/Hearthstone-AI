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
import ANNenums
from tensorflow.contrib import rnn


class RNN(object):
    def __init__(self):
        # Variables
        self.input_size = (ANNenums.GameTag.__len__() * 200) + 150                                                      # Number of input variables
        self.hidden_size = 128                                                                                          # Number of hidden cells
        self.output_size = 30                                                                                           # Number of output variables


        self.RUN_NAME = "Run 20"
        self.endOfGame = True
        self.newGame = True

        # Tesnorflow placeholders
        self.x_placeholder = tf.placeholder(tf.float32, [None, 1, self.input_size])
        self.y_placeholder = tf.placeholder(tf.int32, [None, self.output_size])

        # Weights
        self.weights = tf.Variable(tf.random_normal([self.hidden_size, self.output_size]), dtype=tf.float32)

        # Biases
        self.biases = tf.Variable(tf.random_normal([self.output_size]), dtype=tf.float32)

        def RNN(x, weights, biases):
            lstm_cell = rnn.BasicLSTMCell(self.hidden_size, forget_bias=1.0)                                            # Create a LSTM cell

            outputs, state = tf.nn.dynamic_rnn(lstm_cell, x, dtype=tf.float32,                                          # Create the outputs from LSTM
                                               time_major=True)

            prediction_operation = tf.matmul(outputs[-1], weights) + biases

            return prediction_operation

        self.logits = RNN(self.x_placeholder, self.weights, self.biases)
        self.labels = tf.reshape(self.y_placeholder, [-1])

        # Calculating Loss
        self.prediction_operation = tf.nn.softmax(self.logits)

        self.loss_operation = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=self.y_placeholder)
        self.total_loss_operation = tf.reduce_mean(self.loss_operation)

        self.train_op = tf.train.AdagradOptimizer(0.3).minimize(self.total_loss_operation)

        self.correct_prediction = tf.equal(tf.argmax(self.prediction_operation, 1), tf.argmax(self.y_placeholder, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))

        """ INITIALIZE TENSORFLOW SESSION """
        self.sess = tf.Session()

        init = tf.global_variables_initializer()
        self.sess.run(init)
        self.loss_list = []

    def rec_iter(self, boardState, game):
        while self.index < game.games[-1].export().packets.__len__():
            boardState, self.foundOptions, self.foundSendOptions = self.analyzePacket(
                game.games[-1].export().packets[self.index], boardState)
            self.index += 1
            if self.foundSendOptions or self.foundOptions:
                return boardState
        else:
            self.endOfGame = True
        return boardState

    def generateData(self, boardState, game):
        # This will get the data from the boardState and return it in a readable way by the LSTM network
        self.foundOptions = False
        self.foundSendOptions = False
        if self.newGame:
            self.index = 0
            boardState.reset()
            self.newGame = False

        boardState = self.rec_iter(boardState, game)

        x, y = boardState.get(200)

        x = np.reshape(x, (1, 1, self.input_size))
        y = np.reshape(y, (1, self.output_size))

        # print(x)
        # print(y)

        if self.foundOptions:
            """TODO: Make a prediction"""
            return boardState, x, y
        elif self.foundSendOptions:
            """TODO: Make a test/train epoch"""
            return boardState, x, y
        else:
            self.endOfGame = True
            return boardState, x, y

    def analyzePacket(self, packet, boardState):
        foundOptions = False
        foundSendOptions = False
        if isinstance(packet, packets.Options):
            """ update last options on boardstate """
            boardState.setOptions(packet)
            foundOptions = True
        elif isinstance(packet, packets.SendOption):
            """ update selectedOption on boardstate """
            boardState.setSelectedOptions(packet)
            foundSendOptions = True
        elif isinstance(packet, packets.CreateGame):
            boardState.createGame(packet)
        elif isinstance(packet, packets.FullEntity):
            boardState.addEntity(packet)
        elif isinstance(packet, packets.TagChange):
            boardState.tagChange(packet)
        elif isinstance(packet, packets.ShowEntity):
            boardState.showEntity(packet)
        elif isinstance(packet, packets.Block):
            for pack in packet.__iter__():
                boardState, self.foundOptions, self.foundSendOptions = self.analyzePacket(pack, boardState)
        else:
            print(packet)

        return boardState, foundOptions, foundSendOptions

    def train(self, gui, boardState, game):
        # Takes the Boardstate with possible choices and returns the predicted move,
        # saving the error and updates the network
        boardState, x, y = self.generateData(boardState, game)

        gui.debug("%s", "New data")
        self.sess.run(self.train_op,
                      feed_dict={
                          self.x_placeholder: x,
                          self.y_placeholder: y
                      })

        pred = self.sess.run(self.prediction_operation,
                             feed_dict={
                                 self.x_placeholder: x
                             })
        boardState.setNetworkPrediction(pred)

        # Calculate batch loss and accuracy
        loss, acc, _total_loss = self.sess.run([self.loss_operation, self.accuracy, self.total_loss_operation],
                          feed_dict={
                              self.x_placeholder: x,
                              self.y_placeholder: y
                          })

        self.loss_list.append(_total_loss)

        # if batch_idx % 100 == 0:
        gui.debug("%s", ("Training:", "Loss", _total_loss))

        return boardState

    def test(self, gui, boardState, game):
        """ TODO: Implement """
        # Takes the Boardstate with possible choices and returns the predicted move,
        # saving the error but not updating the network
        boardState, x, y = self.generateData(boardState, game)

    def predict(self, gui, boardState, game):
        """ TODO: Implement """
        # Takes the Boardstate with possible choices and returns the predicted move
        boardState, x, y = self.generateData(boardState, game)

