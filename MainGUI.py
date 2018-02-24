import os
import pyforms
from pyforms import BaseWidget
from pyforms.controls import *
import Network

network = Network.Network()

class HearthGUI(BaseWidget):

    def __init__(self):
        super(HearthGUI, self).__init__('Hearth-AI')

        # Definition of the forms fields
        self._runName = ControlText('Run name')
        self._runButton = ControlButton('Run')
        self._runOnceButton = ControlButton('Run Once')
        self._epochDisplay = ControlButton('Epoch = 0')
        self._boardStateTree = ControlTree('Boar State')
        self._updateBoardState = ControlButton('Update Board State')
        self._readyButton = ControlButton('Ready!')
        self._modeSelect = ControlCombo('Data Loading Mode')

        # Define the actions
        self._runButton.value = self.__runNetwork
        self._runOnceButton.value = self.__runNetworkOnce

        self._modeSelect += ('Randomized Stored Data', 0)
        self._modeSelect += ('Client Connect Windows', 1)
        self._modeSelect += ('Client Connect MacOS', 2)

        self._epochDisplay.enabled = False
        self._readyButton.value = self.__ready
        self._runName.value = network.RUN_NAME

        self.mainmenu = [
            {'File': [
                {'Run Once': self.__runNetworkOnce},
                {'Run': self.__runNetwork},
                '-',
                {'Exit': self._exit},
            ]
            }
        ]

        self.formset = [{
            'a:Options': ['_runName', '_readyButton'],
            'b:Predictions': [''],
            'c:BoardState': ['_boardStateTree', '_updateBoardState']
        },
            '=', ('_runButton', '=', '_runOnceButton'), '||', '_modeSelect']
        # Use dictionaries for tabs
        # Use the sign '=' for a vertical splitter
        # Use the signs '||' for a horizontal splitter

    def _exit(self):
        exit(0)

    def __ready(self):
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

    def __runNetwork(self):
        """Button action event"""
        self._runButton.label = "Running"

    def __runNetworkOnce(self):
        """Button action event"""
        self._runOnceButton.label = "Running"
        self._runOnceButton.enabled = False
        self._runOnceButton.label = "Run Once"
        self._runOnceButton.enabled = True
        mode = self._modeSelect
        print(mode)


#Execute the application
if __name__ == "__main__":   pyforms.start_app(HearthGUI)