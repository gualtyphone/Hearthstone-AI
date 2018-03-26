import os
import pyforms
from pyforms import BaseWidget
from pyforms.controls import *
import Network
import HearthRNN
import BoardState
import cv2

# Creating the network from scratch
network = HearthRNN.RNN()

# Creating Boardstate object
boardState = BoardState.BoardState()

# GUI initialization
class HearthGUI(BaseWidget):

    def __init__(self):
        super(HearthGUI, self).__init__('Hearth-AI')

        # Define Main Menu
        self.mainmenu = [
            {'File': [
                # {'Begin Training': self._train},
                # {'Begin Testing': self._test},
                # {'Begin Predicting': self._predict},
                # '-',
                {'Exit': self._exit},
            ]
            }
        ]

        self.ready = False

        # Definition of the forms fields
        self._runName = ControlText('Run name')
        self._readyButton = ControlButton('Press when ready!')

        self._optionToTakeDescription = ControlText('Play Description')

        self._boardStateTree = ControlTree('Boar State')
        self._updateBoardStateButton = ControlButton('Update Board State')

        self._trainButton = ControlButton('Begin Training')
        self._testButton = ControlButton('Begin Testing')
        self._predictButton = ControlButton('Begin Predicting')

        self._trainButton.enabled = False
        self._testButton.enabled = False
        self._predictButton.enabled = False

        self._epochDisplay = ControlButton('Epoch = 0')
        self._epochSelect = ControlNumber('Epochs to run')
        self._modeSelect = ControlCombo('Data Loading Mode')

        # Define the actions
        self._runName.value = network.RUN_NAME
        self._readyButton.value = self._ready

        self._updateBoardStateButton.value = self._updateBoardState
        self._trainButton.value = self._train
        self._testButton.value = self._test
        self._predictButton.value = self._predict

        self._modeSelect += ('Randomized Stored Data', 0)
        self._modeSelect += ('Client Connect Windows', 1)
        self._modeSelect += ('Client Connect MacOS', 2)

        self._epochDisplay.enabled = False

        self.formset = [{
            'a:Options': ['_runName', '_readyButton'],
            'b:Predictions': ['_optionToTakeDescription'],
            'c:BoardState': ['_boardStateTree']},
            '=',
            ('_modeSelect', '=', '_epochSelect', '=', '_epochDisplay'), '||', ('_trainButton', '=', '_testButton', '=', '_predictButton')
        ]
        # Use dictionaries for tabs
        # Use the sign '=' for a vertical splitter
        # Use the signs '||' for a horizontal splitter

    def _exit(self):
        exit(0)

    def _ready(self):
        """ Check that the runName doesn't already exist """
        if self.ready == False:
            if (os.path.isdir("./logs/" + self._runName.value)):
                #print error
                return
            network.RUN_NAME = self._runName.value
            # Lock the gamemode and Run Name
            self._runName.enabled = False
            self._modeSelect.enabled = False
            self._trainButton.enabled = True
            self._testButton.enabled = True
            self._predictButton.enabled = True
            self.ready = True
            self._readyButton.label = "Finish current Run"
            return
            # prepare the network
        else:
            self._runName.enabled = True
            self._modeSelect.enabled = True
            self._trainButton.enabled = False
            self._testButton.enabled = False
            self._predictButton.enabled = False
            self.ready = False
            self._readyButton.label = "Press when Ready"

    def _train(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def _test(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def _predict(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def _updateBoardState(self):
        """Button action event"""

# Execute the application
if __name__ == "__main__":   pyforms.start_app(HearthGUI)