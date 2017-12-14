import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars

# insert the file you wanna load here
fileName = 'sQXC5MkzFbbDCB3H78YZu8.hsreplay.xml'
pars = Pars()
# load the file to game
# game = hsDoc.from_xml_file(fileName)
while input() != "quit":
    f = open("C:\Program Files (x86)\Hearthstone\Logs\Power.log", "r")
    myList = []
    for line in f:
        myList.append(line)
    f.close()


    pars.read(myList)
    game = hsDoc.from_parser(pars, build=None)

    # load the gameNode that contains the whole game
    gameNode = game.games[-1]

    # in gameNode there are players
    players = gameNode.players

    # players[0] is a hsreplay.elements.PlayerNode
    print(type(players[0]))

    # export() makes the contents readable (apparently)
    print(players[0].export().name)
    print(players[1].export().name)

    # For loop getting all events of the game
    for packet in gameNode.export().recursive_iter():
        print(packet)

    # For loop getting all Blocks Types
    #for packet in gameNode.export().recursive_iter(packets.Block):
    # print(packet)

#whenever you get <options> it's waiting for an action
#after each <options> there is a <SendOptions>