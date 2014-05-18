import pygame
from pygame.locals import *
'''
class TowerGame():
    #Attributes
    __residents = 0
    resRecord = []
    __streak = 0
    __streakTimeLeft = 0.0
    __sway = 0.0
    __floors = 0
    __mistakes = 0

    #Methods
    def getRes(self):
        pass
    def setRes(self, n):
        pass
    def addRes(self, r):
        pass
    def getStreak(self):
        pass
    def setStreak(self, n):
        pass
    def getStreakTime(self):
        pass
    def setStreakTime(self, n):
        pass
    def countdown(self):
        pass
    def getSway(self):
        pass
    def setSway(self, n):
        pass
    def getfloors(self):
        pass
    def addfloors(self, n):
        pass
    def getMistakes(self):
        pass
    def makeMistake(self):
        pass
    def removeLastBlock(self):
        pass




class CityGrid():
    #Attributes
    grid = [[]]
    __totalRes = 0

    #Methods
    def __init__(self):
        pass

    def getRes(self):
        return self.__totalRes

    def addRes(self, n):
        self.__totalRes += n

    def getTower(self, row, col):
        pass

    def placeTower(self, row, col):
        pass

    def delTower(self, row, col):
        pass


'''
class Tower ():
    #Attributes
    __residents = 0
    __colour = 'n'
    __maxLevel = 0
    __maxLevelReached = False
    __topimg = ''
    __midimg = ''
    __bottomimg = ''
    blocklist = []

    #Methods
    def __init__ (self, res):
        self.__residents = res

    def getRes(self):
        return self.__residents

    def addRes(self, n):
        self.__residents += n

    def getcolour(self):
        return self.__colour

    def getMaxLevel(self):
        return self.__maxLevel

    def getReached(self):
        return self.__maxLevelReached

    def setReached(self, b):
        self.__maxLevelReached = b

    def getTopimg(self):
        return self.__topimg

    def getMidimg(self):
        return self.__midimg

    def getBottomimg(self):
        return self.__bottomimg

class BlueTower (Tower):
    #Attributes
    _Tower__colour = 'b'
    _Tower__maxLevel = 10
    _Tower__topimg = "images/Tower/blueTop.png"
    _Tower__midimg = "images/Tower/blueUnit.png"
    _Tower__bottomimg = "images/Tower/blueBase.png"

class RedTower (Tower):
    #Attributes
    _Tower__colour= 'r'
    _Tower__maxLevel = 20
    _Tower__topimg = "images/Tower/redTop.png"
    _Tower__midimg = "images/Tower/redUnit.png"
    _Tower__bottomimg = "images/Tower/redBase.png"

class GreenTower (Tower):
    #Attributes
    _Tower__colour = 'g'
    _Tower__maxLevel = 30
    _Tower__topimg = "images/Tower/greenTop.png"
    _Tower__midimg = "images/Tower/greenUnit.png"
    _Tower__bottomimg = "images/Tower/greenBase.png"

class YellowTower (Tower):
    #Attributes
    _Tower__colour = 'y'
    _Tower__maxLevel = 40
    _Tower__topimg = "images/Tower/yellowTop.png"
    _Tower__midimg = "images/Tower/yellowUnit.png"
    _Tower__bottomimg = "images/Tower/yellowBase.png"

class Block ():
    #Attributes:
    __xPos = 0.0
    __yPos = 0.0
    __res = 0
    __img = ''

    #Methods

    def __init__(self, x, y, res, img):
        self.__xPos = x
        self.__yPos = y
        self.__res = res
        self.__img = img

    def getxPos(self):
        return self.__xPos

    def setxPos(self,x):
        self.__xPos = x

    def getyPos(self):
        return self.__yPos

    def setyPos(self,y):
        self.__yPos = y

    def getRes(self):
        return self.__res

    def setRes(self,res):
        self.__res = res

    def getImg(self):
        return self.__img

    def setImg(self,img):
        self.__img = img
