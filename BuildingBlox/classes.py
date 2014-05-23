'''
Programmer: Benjamin Li
Program Name: BuildingBlox.py (BuildingBlox/__init__.py)
Project Name: City Manager
Purpose: Main file for the Building Blox game. Includes tower building and menu interfaces
Date: May 20, 2014
'''

# Superclass for the types of towers in the game
class Tower ():

    #Attributes
    __maxLevel = 0  # integer, the number of floors the tower can have at maximum
    __topimg = ''  # string, file directory for the image for the top block
    __midimg = ''  # string, file directory for the image for the middle blocks
    __bottomimg = ''  # string, file directory for the image for the bottom block

    #Methods
    # Accessor method for the number of maximum levels
    def getMaxLevel(self):
        return self.__maxLevel

    # Accessor method for the top block image directory
    def getTopimg(self):
        return self.__topimg

    # Accessor method for the middle block image directory
    def getMidimg(self):
        return self.__midimg

    # Accessor method for the bottom block image directory
    def getBottomimg(self):
        return self.__bottomimg

# Class for the blue apartment tower (10 floors), inherits from Tower
class BlueTower (Tower):
    #Attributes
    _Tower__maxLevel = 10
    _Tower__topimg = "images/Tower/blueTop.png"
    _Tower__midimg = "images/Tower/blueUnit.png"
    _Tower__bottomimg = "images/Tower/blueBase.png"


# Class for the red condo tower (20 floors), inherits from Tower
class RedTower (Tower):
    #Attributes
    _Tower__maxLevel = 20
    _Tower__topimg = "images/Tower/redTop.png"
    _Tower__midimg = "images/Tower/redUnit.png"
    _Tower__bottomimg = "images/Tower/redBase.png"


# Class for the green complex tower (30 floors), inherits from Tower
class GreenTower (Tower):
    #Attributes
    _Tower__maxLevel = 30
    _Tower__topimg = "images/Tower/greenTop.png"
    _Tower__midimg = "images/Tower/greenUnit.png"
    _Tower__bottomimg = "images/Tower/greenBase.png"


# Class for the yellow skyscraper tower (30 floors), inherits from Tower
class YellowTower (Tower):
    #Attributes
    _Tower__maxLevel = 40
    _Tower__topimg = "images/Tower/yellowTop.png"
    _Tower__midimg = "images/Tower/yellowUnit.png"
    _Tower__bottomimg = "images/Tower/yellowBase.png"


# Class that represents one block in a tower
class Block ():

    #Attributes:
    __xPos = 0.0  # float, the current horizontal coordinate of the block
    __yPos = 0.0  # float, the current vertical coordinate of the block
    __res = 0  # integer, the number of residents (score) earned from this block
    __img = ''  # string, the directory of the image that represents the block

    #Methods
    # Initializes the object with information of the current block to be stored into a list
    def __init__(self, x, y, res, img):
        self.__xPos = x
        self.__yPos = y
        self.__res = res
        self.__img = img

    # Accessor method for the horizontal position
    def getxPos(self):
        return self.__xPos

    # Modifier method for the horizontal position
    def setxPos(self,x):
        self.__xPos = x

    # Accessor method for the vertical position
    def getyPos(self):
        return self.__yPos

    # Modifier method for the vertical position
    def setyPos(self,y):
        self.__yPos = y

    # Accessor method for the number of residents (Score)
    def getRes(self):
        return self.__res

    # Modifier method for the number of residents (Score)
    def setRes(self,res):
        self.__res = res

    # Accessor method for the block image file directory
    def getImg(self):
        return self.__img

    # Modifier method for the block image file directory
    def setImg(self,img):
        self.__img = img
