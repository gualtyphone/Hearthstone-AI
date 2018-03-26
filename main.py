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

""" MAIN LOOP """
while running:

    gui.Draw()
    running = gui.running

    # If the gui says to run the network
    # TRAIN MODE
    if gui.trainMode:
        gameLoader.Update()
        # If the mode is "Get from running HS"
        if gui.dataLoadingMode == 1 | gui.dataLoadingMode == 2:
            # if there is an update to analyze
            if gameLoader.gameUpdated:
                network.train(gui)
        else:
            # if the network has epochs to run
            if int(gui.frames[Options].epochsToRun.get()) > currentEpochCount:
                # Load next Game
                if gameLoader.gameUpdated:
                    # Run next epoch
                    network.train(gui)
                    gui.Plot(network)
                # Increase the epoch count
                currentEpochCount += 1
            else:
                gui.stopNetwork()
                currentEpochCount = 0

    # TEST MODE
    elif gui.testMode:
        gameLoader.Update()
        # If the mode is "Get from running HS"
        if gui.dataLoadingMode == 1 | gui.dataLoadingMode == 2:
            # if there is an update to analyze
            if gameLoader.gameUpdated:
                network.test()
        else:
            # if the network has epochs to run
            if int(gui.frames[Options].epochsToRun.get()) > currentEpochCount:
                # Load next Game
                if gameLoader.gameUpdated:
                    # Run next epoch
                    network.test()
                    gui.Plot(network)
                # Increase the epoch count
                currentEpochCount += 1
            else:
                gui.stopNetwork()
                currentEpochCount = 0
    # PREDICT MODE
    elif gui.predictMode:
        gameLoader.Update()
        # If the mode is "Get from running HS"
        if gui.dataLoadingMode == 1 | gui.dataLoadingMode == 2:
            # if there is an update to analyze
            if gameLoader.gameUpdated:
                network.predict()
        else:
            # if the network has epochs to run
            if int(gui.frames[Options].epochsToRun.get()) > currentEpochCount:
                # Load next Game
                if gameLoader.gameUpdated:
                    # Run next epoch
                    network.predict()
                # Increase the epoch count
                currentEpochCount += 1
            else:
                gui.stopNetwork()
                currentEpochCount = 0


""" DESTRUCTOR """
print("Quitting")
