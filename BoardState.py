import os
import hearthstone as hs
from hsreplay.document import HSReplayDocument as hsDoc
from hslog import packets
from hslog.parser import LogParser as Pars
import numpy as np
import ANNenums


class BoardState(object):

    stateDict = {}

    def __init__(self):
        print("Creating Board state")
        self.stateDict = {}
        # The various objects will be stored as a ID, Array of tags dictionary
        x = 1
        while x <= 3:
            self.stateDict[x] = {}
            for tag in ANNenums.GameTag:
                self.stateDict[x][tag] = 0
            x += 1

    def addEntity(self, entity):
        # print(type(entity.entity))
        self.stateDict[entity.entity] = {}
        for tag in ANNenums.GameTag:
            self.stateDict[entity.entity][tag] = 0
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]

    def tagChange(self, tagChanged):
        # print("TagChange")
        self.stateDict[tagChanged.entity][tagChanged.tag] = tagChanged.value

    def showEntity(self, entity):
        for tag in entity.tags:
            self.stateDict[entity.entity][tag[0]] = tag[1]


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