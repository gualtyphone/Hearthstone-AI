import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import BoardState
import numpy as np
import GameLoader

# For Tensorboard, in terminal: tensorboard --logdir=logs

# 0 - Logs, 1- Client Connect PC, 2 - Client Connect MAC
mode = 0

# Turn off TensorFlow warning messages in program output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- Create Neural Network ---

# Define model parameters
learning_rate = 0.001

# Define how many inputs and outputs are in our neural network
number_of_inputs = 25350
number_of_outputs = 30

# Define how many neurons we want in each layer of our neural network
layer_1_nodes = 50
layer_2_nodes = 100
layer_3_nodes = 50

# Section One: Define the layers of the neural network itself

# Input Layer
with tf.variable_scope('input'):
    X = tf.placeholder(tf.float32, shape=(None, number_of_inputs))

# Layer 1
with tf.variable_scope('layer_1'):
    weights = tf.get_variable("weights1", shape=[number_of_inputs, layer_1_nodes], initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases1", shape=[layer_1_nodes], initializer=tf.zeros_initializer())
    layer_1_output = tf.nn.relu(tf.matmul(X, weights) + biases)

# Layer 2
with tf.variable_scope('layer_2'):
    weights = tf.get_variable("weights2", shape=[layer_1_nodes, layer_2_nodes], initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases2", shape=[layer_2_nodes], initializer=tf.zeros_initializer())
    layer_2_output = tf.nn.relu(tf.matmul(layer_1_output, weights) + biases)

# Layer 3
with tf.variable_scope('layer_3'):
    weights = tf.get_variable("weights3", shape=[layer_2_nodes, layer_3_nodes], initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases3", shape=[layer_3_nodes], initializer=tf.zeros_initializer())
    layer_3_output = tf.nn.relu(tf.matmul(layer_2_output, weights) + biases)

# Output Layer
with tf.variable_scope('output'):
    weights = tf.get_variable("weights4", shape=[layer_3_nodes, number_of_outputs], initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases4", shape=[number_of_outputs], initializer=tf.zeros_initializer())
    prediction = tf.matmul(layer_3_output, weights) + biases

# Section Two: Define the cost function of the neural network that will measure prediction accuracy during training

with tf.variable_scope('cost'):
    Y = tf.placeholder(tf.float32, shape=(None, number_of_outputs))
    cost = tf.reduce_mean(tf.squared_difference(prediction, Y))

# Section Three: Define the optimizer function that will be run to optimize the neural network

with tf.variable_scope('train'):
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# Create a summary operation to log the progress of the network
with tf.variable_scope('logging'):
    tf.summary.scalar('current_cost', cost)
    summary = tf.summary.merge_all()

epoch = 0

RUN_NAME = "Run 14"

def modeloop(mode):
    if mode == 0:
        return 1
    else:
        return input() != quit


# --- Main Loop ---
with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    training_writer = tf.summary.FileWriter("./logs/{}/training".format(RUN_NAME), session.graph)

    mode = int(input("Select Game Loading Mode (0 - Logs, 1- Client Connect PC, 2 - Client Connect MAC):"))

    while modeloop(mode):

        game = None

        if mode == 0:
            game = GameLoader.LoadRandomizedLog()
        elif mode == 1:
            game = GameLoader.loadPcGame()
        else:
            game = GameLoader.loadMacGame()

        # --- Crate The BoardState object ---

        boardState = BoardState.BoardState

        # load the gameNode that contains the whole game
        gameNode = game.games[-1]

        # in gameNode there are players
        players = gameNode.players

        # players[0] is a hsreplay.elements.PlayerNode
        # print(type(players[0]))

        print("Using Game between {} and {}".format(players[0].export().name, players[1].export().name))

        lastOptions = packets.Options

        def _iter_recursive(_packets, epoch):
            for packet in _packets:
                # find the type of packet
                if isinstance(packet, packets.Options):
                    lastOptions = packet
                    # print("Options")
                    # for option in packet.options:
                    #     print("Option:", option.entity)
                    # load the curent state in the network
                    # run the network and get the desired output
                    feed_dict = {X: (boardState.get(boardState, 100, lastOptions).reshape(1, number_of_inputs))}
                    scaled_predicted = session.run(prediction, feed_dict=feed_dict)

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
                    options = np.zeros(number_of_outputs)
                    options[packet.option] = 10
                    # print("SelectedOption:", packet.option)
                    # print("SelectedSubOption:", packet.suboption)
                    # print("SelectedEntity:", packet.entity)
                    # print("FoundOption:", lastOption.options[packet.option].entity)
                    # compare with the network stored send options
                    # train network X is input, Y is output
                    feed_dict = {X: (boardState.get(boardState, 100, lastOptions).reshape(1, number_of_inputs))}
                    scaled_predicted = session.run(prediction, feed_dict=feed_dict)

                    feed_dict = {X: (boardState.get(boardState, 100, lastOptions).reshape(1, number_of_inputs)),
                                 Y: options.reshape(1, 30)}
                    session.run(optimizer, feed_dict=feed_dict)

                    training_cost, training_summary = session.run([cost, summary], feed_dict=feed_dict)
                    training_writer.add_summary(training_summary, epoch)
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
                        boardState.__init__(boardState)
                    elif isinstance(packet, packets.FullEntity):
                        boardState.addEntity(boardState, packet)
                    elif isinstance(packet, packets.TagChange):
                        boardState.tagChange(boardState, packet)
                    elif isinstance(packet, packets.ShowEntity):
                        boardState.showEntity(boardState, packet)
                    elif isinstance(packet, packets.MetaData):
                        continue
                    elif isinstance(packet, packets.Block):
                        epoch = _iter_recursive(packet.packets, epoch)
                    else:
                        print(packet)
            return epoch

        epoch = _iter_recursive(gameNode.export(), epoch)
        epoch += 1

        # boardState.print(boardState)

        print("End Of Loop")