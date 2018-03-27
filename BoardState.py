import os
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import numpy as np
import ANNenums


class BoardState(object):

    def __init__(self):
        self.stateDict = {}
        self.board = list()
        self.options = list()
        for i in range(100):
            self.board.append("")
        self.optionsPacket = None
        self.selectedOptions = {}
        self.reset()

    def reset(self):
        print("Resetting Board state")
        # The various objects will be stored as a ID, Array of tags dictionary

        self.board.clear()
        for i in range(100):
            self.board.append("")
        self.board[0] = "EndTurnButton"
        self.board[1] = "GameReference"
        self.board[2] = "Player1Reference"
        self.board[3] = "Player2Reference"
        x = 1
        while x <= 3:
            self.stateDict[x] = {}
            for tag in ANNenums.GameTag:
                self.stateDict[x][tag] = 0
            x += 1

    def createGame(self, gamePacket):
        print("creating Board state")
        # The various objects will be stored as a ID, Array of tags dictionary

        self.board.clear()
        for i in range(100):
            self.board.append("")
        self.board[0] = "EndTurnButton"
        self.board[1] = "GameReference"
        self.board[2] = "Player: " + gamePacket.players[0].name
        self.board[3] = "Player: " + gamePacket.players[1].name
        x = 1
        while x <= 3:
            self.stateDict[x] = {}
            for tag in ANNenums.GameTag:
                self.stateDict[x][tag] = 0
            x += 1

    def addEntity(self, entity):
        # print(type(entity.entity))
        self.stateDict[entity.entity] = {}
        self.board[entity.entity] = entity.card_id
        # self.board[entity.entity] = entity.card_id
        for tag in ANNenums.GameTag:
            self.stateDict[entity.entity][tag] = 0
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]

    def tagChange(self, tagChanged):
        # print("TagChange")
        self.stateDict[tagChanged.entity][tagChanged.tag] = tagChanged.value

    def showEntity(self, entity):
        self.board[entity.entity] = entity.card_id
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]

    def getOptions(self):
        # Return the options in a good format
        """TODO: Implement"""
        return self.options

    def setOptions(self, packet):
        """TODO: Implement"""
        self.options.clear()
        for opt in packet.options:
            optionDescriptor = (opt.id, " - ", opt.entity, self.board[opt.entity], opt.type)
            self.options.append(optionDescriptor)

    def setSelectedOptions(self, packet):
        """TODO: Implement"""

    def get(self, numberOfEntities, lastOptions):
        result = np.zeros(int((ANNenums.GameTag.__len__() * numberOfEntities) + 150))
        y = 0
        for opt in lastOptions.options:
            result[y] = opt.entity
            y += 1
            result[y] = opt.id
            y += 1
            result[y] = opt.type
            y += 1
            if (opt.error == None):
                result[y] = 0
            else:
                result[y] = opt.error
            y += 1
            if (opt.error_param == None):
                result[y] = 0
            else:
                result[y] = opt.error_param
            y += 1
        for k in sorted(self.stateDict.keys()):
            # row = []
            i = 0
            for k1 in sorted(self.stateDict[k].keys()):
                # print (ANNenums.GameTag.__len__())
                result[k*ANNenums.GameTag.__len__() + i + 150] = (self.stateDict[k][k1])
                i += 1
            # result.append(row)
        # for i in result:
        #     print(i)
        # print(result)
        return result

    def print(self):
        result = []
        for k in sorted(self.stateDict.keys()):
            row = []
            for k1 in sorted(self.stateDict[k].keys()):
                # print (ANNenums.GameTag.__len__())
                row.append (self.stateDict[k][k1])
            result.append(row)
        for i in result:
            print(i)
        # print(result)