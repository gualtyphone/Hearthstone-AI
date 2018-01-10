import os
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import numpy as np

class BoardState:

    stateDict = {}

    def __init__(self):
        print("Creating Board state")
        # The various objects will be stored as a ID, Array of tags dictionary
        x = 1
        while x <= 3:
            self.stateDict[x] = {}
            i = 0
            while i < 1000:
                self.stateDict[x][i] = 0
                i += 1
            x += 1

    def addEntity(self, entity):
        # print(type(entity.entity))
        self.stateDict[entity.entity] = {}
        i = 0
        while i < 1000:
            self.stateDict[entity.entity][i] = 0
            i += 1
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]

    def tagChange(self, tagChanged):
        # print("TagChange")
        self.stateDict[tagChanged.entity][tagChanged.tag] = tagChanged.value

    def showEntity(self, entity):
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]

    def get(self, numberOfEntities):
        result = np.zeros((100000))
        for k in sorted(self.stateDict.keys()):
            # row = []
            for k1 in sorted(self.stateDict[k].keys()):
                result[k*1000 + k1] = (self.stateDict[k][k1])
            # result.append(row)
        # for i in result:
        #     print(i)
        print(result)
        return result