import os
import random
from hsreplay.document import HSReplayDocument as hsDoc
from hslog.parser import LogParser as Pars

class GameLoader(object):

    def __init__(self):
        self.mode = 0
        self.previousGame = None
        self.game = None

        self.gameUpdated = False

        self.newGame = False

    def Update(self, dataLoadingMode):
        self.mode = dataLoadingMode
        self.previousGame = self.game
        if  self.mode == 0:
            self.game = self.loadRandomizedLog()
            self.newGame = True
        elif self.mode == 1:
            self.game = self.loadPcGame()
            self.newGame = self.checkNewGame()
        elif self.mode == 2:
            self.game = self.loadMacGame()
            self.newGame = self.checkNewGame()
        if self.previousGame == self.game:
            self.gameUpdated = False
            return

        self.on_game_updated()

    def checkNewGame(self):
        if self.previousGame.game.games[-1].players[0].export().name == self.game.game.games[-1].players[0].export().name:
            if self.previousGame.game.games[-1].players[1].export().name == self.game.game.games[-1].players[1].export().name:
                #Same players, assuming same game
                self.newGame = False
                return
        # Different players, surely different game
        self.newGame = True
        return

    def on_game_updated(self):
        self.gameUpdated = True

    def loadMacGame(self):

        f = open("/Applications/Hearthstone/Logs/Power.log", "r")
        myList = []
        for line in f:
            myList.append(line)
        f.close()

        pars = Pars()
        pars.read(myList)
        game = hsDoc.from_parser(pars, build=None)
        return game

    def loadPcGame(self):

        # --- Connect to Hearthstone Client Directly ---
        f = open("C:\Program Files (x86)\Hearthstone\Logs\Power.log", "r")
        myList = []
        for line in f:
            myList.append(line)
        f.close()

        pars = Pars()
        pars.read(myList)
        game = hsDoc.from_parser(pars, build=None)
        return game

    def loadRandomizedLog(self):

        # --- Load the folder to search files in ---
        folderPath = "./Games/Standardized/"
        xmlFiles = [os.path.join(root, name)
                     for root, dirs, files in os.walk(folderPath)
                     for name in files
                     if name.endswith((".xml"))]

        fileName = random.choice(xmlFiles)

        # load the file to game
        game = hsDoc.from_xml_file(fileName)
        return game