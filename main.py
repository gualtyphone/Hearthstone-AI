# Import all that is needed
from GUI import *
from BoardState import BoardState
from HearthRNN import RNN
from GameLoader import GameLoader

""" GLOBAL VARIABLES """
running = True
gui = GUI()
boardState = BoardState()
network = RNN()
gameLoader = GameLoader()

""" MAIN LOOP """
while running:
    gameLoader.Update()

    gui.Plot(network)

    gui.Draw()
    running = gui.running

""" DESTRUCTOR """
print("Quitting")
