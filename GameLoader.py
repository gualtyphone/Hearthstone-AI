import os
import random
from hsreplay.document import HSReplayDocument as hsDoc
from hslog.parser import LogParser as Pars


def loadMacGame():

    f = open("/Applications/Hearthstone/Logs/Power.log", "r")
    myList = []
    for line in f:
        myList.append(line)
    f.close()

    pars = Pars()
    pars.read(myList)
    game = hsDoc.from_parser(pars, build=None)
    return game

def loadPcGame():

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

def LoadRandomizedLog():

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