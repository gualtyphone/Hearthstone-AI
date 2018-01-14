import os
import tensorflow as tf
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars

pars = Pars()

f = open("C:\Program Files (x86)\Hearthstone\Logs\Power.log", "r")
myList = []
for line in f:
    myList.append(line)
f.close()

pars.read(myList)
game = hsDoc.from_parser(pars, build=None)

# load the gameNode that contains the whole game
gameNode = game.games[-1]