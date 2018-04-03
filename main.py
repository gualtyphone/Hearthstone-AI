# Import all that is needed
from HS_GUI import *
from BoardState import BoardState
from HearthRNN import RNN
from GameLoader import GameLoader

""" GLOBAL VARIABLES """
running = True
gui = HS_GUI()
boardState = BoardState()
network = RNN()
gameLoader = GameLoader()

currentEpochCount = 0

def runNetwork(currentEpochCount, boardState):
    # If the mode is "Get from running HS"
    if gui.dataLoadingMode == 1 or gui.dataLoadingMode == 2:
        if gui.trainMode:
            boardState = network.train(gui, boardState, gameLoader.game)
        if gui.testMode:
            boardState = network.test(gui, boardState, gameLoader.game)
        if gui.predictMode:
            boardState = network.predict(gui, boardState, gameLoader.game)
        gui.Plot(network)
    else:
        # if the network has epochs to run
        if int(gui.frames[Options].epochsToRun.get()) > currentEpochCount:
            # Run next epoch
            if gui.trainMode:
                boardState = network.train(gui, boardState, gameLoader.game)
            if gui.testMode:
                boardState = network.test(gui, boardState, gameLoader.game)
            if gui.predictMode:
                boardState = network.predict(gui, boardState, gameLoader.game)
            gui.Plot(network)
            # Increase the epoch count
            if network.endOfGame:
                currentEpochCount += 1
        else:
            gui.stopNetwork()
            currentEpochCount = 0

    return currentEpochCount, boardState

""" MAIN LOOP """
while running:

    gui.Draw()
    running = gui.running

    # If the gui says to run the network
    if gui.trainMode or gui.testMode or gui.predictMode:
        if network.endOfGame:
            # Check Game for update
            # boardState.reset()
            gameLoader.Update(gui.dataLoadingMode)
            # if there is an update to analyze
            if gameLoader.gameUpdated:
                network.endOfGame = False
                network.newGame = True
                currentEpochCount, boardState = runNetwork(currentEpochCount, boardState)
                gui.displayOptionsAndBoard(boardState)
                gameLoader.gameUpdated = False
        else:
            #Network hasn't finished current game
                currentEpochCount, boardState = runNetwork(currentEpochCount, boardState)
                gui.displayOptionsAndBoard(boardState)

""" DESTRUCTOR """
print("Quitting")
