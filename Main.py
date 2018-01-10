import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import BoardState
import numpy as np

# Turn off TensorFlow warning messages in program output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- Create Game File ---

# insert the file you wanna load here
fileName = 'sQXC5MkzFbbDCB3H78YZu8.hsreplay.xml'
pars = Pars()
# load the file to game
game = hsDoc.from_xml_file(fileName)

# --- Crate The BoardState object ---

boardState = BoardState.BoardState

# --- Create Neural Network ---

# Define model parameters
learning_rate = 0.001

# Define how many inputs and outputs are in our neural network
number_of_inputs = 100000
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
    Y = tf.placeholder(tf.float32, shape=(None, 1))
    cost = tf.reduce_mean(tf.squared_difference(prediction, Y))

# Section Three: Define the optimizer function that will be run to optimize the neural network

with tf.variable_scope('train'):
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# Create a summary operation to log the progress of the network
with tf.variable_scope('logging'):
    tf.summary.scalar('current_cost', cost)
    summary = tf.summary.merge_all()


# --- Main Loop ---

while input() != "quit":
    # f = open("C:\Program Files (x86)\Hearthstone\Logs\Power.log", "r")
    # myList = []
    # for line in f:
    #     myList.append(line)
    # f.close()
    #
    #
    # pars.read(myList)
    # game = hsDoc.from_parser(pars, build=None)

    # load the gameNode that contains the whole game
    gameNode = game.games[-1]

    # in gameNode there are players
    players = gameNode.players

    # players[0] is a hsreplay.elements.PlayerNode
    print(type(players[0]))

    # export() makes the contents readable (apparently)
    print(players[0].export().name)
    print(players[1].export().name)

    lastOption = packets.Options

    with tf.Session() as session:

        session.run(tf.global_variables_initializer())



        # For loop getting all events of the game

        def _iter_recursive(_packets):
            for packet in _packets:
                # find the type of packet
                if isinstance(packet, packets.Options):
                    lastOption = packet
                    # print("Options")
                    # for option in packet.options:
                    #     print("Option:", option.entity)
                    # load the curent state in the network
                    # run the network and get the desired output
                    scaled_predicted = session.run(prediction, feed_dict={X: (boardState.get(boardState, number_of_inputs/1000).reshape(1, 100000))})
                    # predicted = scaler.inverse_transform(scaled_predicted)
                    # display output
                    print(scaled_predicted)

                elif isinstance(packet, packets.SendOption):
                    lastOption = packet
                    # print("sendOptions")
                    # print("SelectedOption:", packet.option)
                    # print("SelectedSubOption:", packet.suboption)
                    # print("SelectedEntity:", packet.entity)
                    # print("FoundOption:", lastOption.options[packet.option].entity)
                    # compare with the network stored send options
                    # train network
                    # session.run(optimizer, feed_dict={})

                else:
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
                        _iter_recursive(packet.packets)
                    else:
                        print(packet)
                    # update the board state tensor

        _iter_recursive(gameNode.export())

        boardState.get(boardState, number_of_inputs/1000)

        print("EndOfLoop")
        # For loop getting all Blocks Types
        # for packet in gameNode.export().recursive_iter(packets.Block):
        # print(packet)

#whenever you get <options> it's waiting for an action
#after each <options> there is a <SendOptions>