import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import BoardState
import numpy as np
import GameLoader


class Network(object):
    def __init__(self):
        self.mode = 0
        self.epoch = 0
        self.RUN_NAME = "Run 14"

        self.is_ready = False

        # Turn off TensorFlow warning messages in program output
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        # --- Create Neural Network ---

        # Define model parameters
        self.learning_rate = 0.001

        # Define how many inputs and outputs are in our neural network
        self.number_of_inputs = 25350
        self.number_of_outputs = 30

        # Define how many neurons we want in each layer of our neural network
        self.layer_1_nodes = 50
        self.layer_2_nodes = 100
        self.layer_3_nodes = 50

        # Section One: Define the layers of the neural network itself

        # Input Layer
        with tf.variable_scope('input'):
            self.X = tf.placeholder(tf.float32, shape=(None, self.number_of_inputs))

        # Layer 1
        with tf.variable_scope('layer_1'):
            weights = tf.get_variable("weights1", shape=[self.number_of_inputs, self.layer_1_nodes], initializer=tf.contrib.layers.xavier_initializer())
            biases = tf.get_variable(name="biases1", shape=[self.layer_1_nodes], initializer=tf.zeros_initializer())
            self.layer_1_output = tf.nn.relu(tf.matmul(self.X, weights) + biases)

        # Layer 2
        with tf.variable_scope('layer_2'):
            weights = tf.get_variable("weights2", shape=[self.layer_1_nodes, self.layer_2_nodes], initializer=tf.contrib.layers.xavier_initializer())
            biases = tf.get_variable(name="biases2", shape=[self.layer_2_nodes], initializer=tf.zeros_initializer())
            self.layer_2_output = tf.nn.relu(tf.matmul(self.layer_1_output, weights) + biases)

        # Layer 3
        with tf.variable_scope('layer_3'):
            weights = tf.get_variable("weights3", shape=[self.layer_2_nodes, self.layer_3_nodes], initializer=tf.contrib.layers.xavier_initializer())
            biases = tf.get_variable(name="biases3", shape=[self.layer_3_nodes], initializer=tf.zeros_initializer())
            self.layer_3_output = tf.nn.relu(tf.matmul(self.layer_2_output, weights) + biases)

        # Output Layer
        with tf.variable_scope('output'):
            weights = tf.get_variable("weights4", shape=[self.layer_3_nodes, self.number_of_outputs], initializer=tf.contrib.layers.xavier_initializer())
            biases = tf.get_variable(name="biases4", shape=[self.number_of_outputs], initializer=tf.zeros_initializer())
            self.prediction = tf.matmul(self.layer_3_output, weights) + biases

        # Section Two: Define the cost function of the neural network that will measure prediction accuracy during training

        with tf.variable_scope('cost'):
            self.Y = tf.placeholder(tf.float32, shape=(None, self.number_of_outputs))
            self.cost = tf.reduce_mean(tf.squared_difference(self.prediction, self.Y))

        # Section Three: Define the optimizer function that will be run to optimize the neural network

        with tf.variable_scope('train'):
            self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cost)

        # Create a summary operation to log the progress of the network
        with tf.variable_scope('logging'):
            tf.summary.scalar('current_cost', self.cost)
            self.summary = tf.summary.merge_all()

        self.session = tf.Session()
        self.training_writer = None

    def ready(self):
        # --- Main Loop ---
        self.is_ready = True

        self.session.run(tf.global_variables_initializer())
        self.training_writer = tf.summary.FileWriter("./logs/{}/training".format(self.RUN_NAME), self.session.graph)

    def _singleRun(self):
        if not self.is_ready:
            return

        self.game = None

        if self.mode == 0:
            self.game = GameLoader.LoadRandomizedLog()
        elif self.mode == 1:
            self.game = GameLoader.loadPcGame()
        else:
            self.game = GameLoader.loadMacGame()

        # --- Crate The BoardState object ---

        self.boardState = BoardState.BoardState()

        # load the gameNode that contains the whole game
        self.gameNode = self.game.games[-1]

        # in gameNode there are players
        self.players = self.gameNode.players

        # players[0] is a hsreplay.elements.PlayerNode
        # print(type(players[0]))

        print("Using Game between {} and {}".format(self.players[0].export().name, self.players[1].export().name))

        self.lastOptions = packets.Options


    def _iter_recursive(self, _packets):
        for packet in _packets:
            # find the type of packet
            if isinstance(packet, packets.Options):
                lastOptions = packet
                # print("Options")
                # for option in packet.options:
                #     print("Option:", option.entity)
                # load the curent state in the network
                # run the network and get the desired output
                feed_dict = {self.X: (self.boardState.get(100, lastOptions).reshape(1, self.number_of_inputs))}
                scaled_predicted = self.session.run(self.prediction, feed_dict=feed_dict)

                best = 0.0
                final = 0
                for idx, val in enumerate(scaled_predicted[0]):
                    if val > best:
                        best = val
                        final = idx

                if final < packet.options.__len__():
                    print("Network Predicts: option {}, entity {}".format(final, packet.options[final].entity))
                    # (packet.options[final].type)
                    # print(packet.options[final].optype)
                    # for opt in packet.options[final].options:
                    #     print(opt)
                else:
                    print("Inexistent prediction")


                # predicted = scaler.inverse_transform(scaled_predicted)
                # display output
                # print(scaled_predicted)

            elif isinstance(packet, packets.SendOption):
                # print("Send Options")
                options = np.zeros(self.number_of_outputs)
                options[packet.option] = 10
                # print("SelectedOption:", packet.option)
                # print("SelectedSubOption:", packet.suboption)
                # print("SelectedEntity:", packet.entity)
                # print("FoundOption:", lastOption.options[packet.option].entity)
                # compare with the network stored send options
                # train network X is input, Y is output
                feed_dict = {self.X: (self.boardState.get(100, lastOptions).reshape(1, self.number_of_inputs))}
                scaled_predicted = self.session.run(self.prediction, feed_dict=feed_dict)

                feed_dict = {self.X: (self.boardState.get(100, lastOptions).reshape(1, self.number_of_inputs)),
                             self.Y: options.reshape(1, 30)}
                self.session.run(self.optimizer, feed_dict=feed_dict)

                training_cost, training_summary = self.session.run([self.cost, self.summary], feed_dict=feed_dict)
                self.training_writer.add_summary(training_summary, self.epoch)
                # print("Training Cost: {}".format(training_cost))


                best = 0.0
                final = 0
                for idx, val in enumerate(scaled_predicted[0]):
                    if val > best:
                        best = val
                        final = idx

                if final < lastOptions.options.__len__():
                    print("The network chooses: {} ; The player chooses: {}".format(final, packet.option))
                    # for opt in packet.options[final].options:
                    #     print(opt)
                else:
                    print("Inexistent prediction")

            else:
                # update the board state tensor
                if isinstance(packet, packets.CreateGame):
                    self.boardState.__init__()
                elif isinstance(packet, packets.FullEntity):
                    self.boardState.addEntity(packet)
                elif isinstance(packet, packets.TagChange):
                    self.boardState.tagChange(packet)
                elif isinstance(packet, packets.ShowEntity):
                    self.boardState.showEntity(packet)
                elif isinstance(packet, packets.MetaData):
                    continue
                elif isinstance(packet, packets.Block):
                    self.epoch = self._iter_recursive(packet.packets)
                else:
                    print(packet)