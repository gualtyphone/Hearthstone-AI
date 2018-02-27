import os
import pyforms
from pyforms import BaseWidget
from pyforms.controls import *
import Network
import cv2

network = Network.Network()

class HearthGUI(BaseWidget):

    def __init__(self):
        super(HearthGUI, self).__init__('Hearth-AI')

        # Define Main Menu
        self.mainmenu = [
            {'File': [
                {'Run Once': self._runNetworkOnce},
                {'Run': self._runNetwork},
                '-',
                {'Exit': self._exit},
            ]
            }
        ]

        # Definition of the forms fields
        self._runName = ControlText('Run name')
        self._readyButton = ControlButton('Press when ready!')

        self._cardToPlayImage = ControlImage()
        self._cardToPlayGL = ControlOpenGL()
        self._optionToTakeDescription = ControlText('Play Description')

        self._boardStateTree = ControlTree('Boar State')
        self._updateBoardStateButton = ControlButton('Update Board State')

        self._runButton = ControlButton('Run')
        self._runOnceButton = ControlButton('Run Once')
        self._epochDisplay = ControlButton('Epoch = 0')
        self._modeSelect = ControlCombo('Data Loading Mode')

        # Define the actions
        self._runName.value = network.RUN_NAME
        self._readyButton.value = self._ready

        self._cardToPlayImage.value = cv2.imread('Cards/Alex.png', 1)
        self._cardToPlayImage.repaint()

        self._updateBoardStateButton.value = self._updateBoardState
        self._runButton.value = self._runNetwork
        self._runOnceButton.value = self._runNetworkOnce

        self._modeSelect += ('Randomized Stored Data', 0)
        self._modeSelect += ('Client Connect Windows', 1)
        self._modeSelect += ('Client Connect MacOS', 2)

        self._epochDisplay.enabled = False

        self.formset = [{
            'a:Options': ['_runName', '_readyButton'],
            'b:Predictions': [(), '||', ('_cardToPlayImage', '_cardToPlayGL', '_optionToTakeDescription')],
            'c:BoardState': ['_boardStateTree', '_updateBoardStateButton']},
            '=',
            ('_runButton', '=', '_runOnceButton'), '||', '_modeSelect'
        ]
        # Use dictionaries for tabs
        # Use the sign '=' for a vertical splitter
        # Use the signs '||' for a horizontal splitter

    def _exit(self):
        exit(0)

    def _ready(self):
        """ Check that the runName doesn't already exist """
        if (os.path.isdir("./logs/" + self._runName.value)):
            #print error
            return
        network.RUN_NAME = self._runName.value
        # Lock the gamemode and Run Name
        self._runName.enabled = False
        self._modeSelect.enabled = False
        # prepare the network
        network.ready()
        # Run a first loop

    def _runNetwork(self):
        """Button action event"""
        self._runButton.label = "Running"

    def _runNetworkOnce(self):
        """Button action event"""
        self._runOnceButton.label = "Running"
        self._runOnceButton.enabled = False
        self._runOnceButton.label = "Run Once"
        self._runOnceButton.enabled = True
        mode = self._modeSelect
        print(mode)

    def _updateBoardState(self):
        """Button action event"""

#Execute the application
if __name__ == "__main__":   pyforms.start_app(HearthGUI)