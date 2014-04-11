import pygame
from pygame.locals import *
import ConfigParser
import os
scriptDir = os.path.dirname(__file__)

class Player():
    def __init__(self):
        self.highScore = 0
        self.position = [0,0]
    def setHighScore(self, highScore):
        self.highScore = highScore

class City():
    def __init__(self, size, population):
        self.size = size
        self.population = population
    def increasePopulation(self):
        pass
class Car():
    def __init__(self):
        self.speed = 0
        self.direction = "N"
        self.position = [0,0]
    def setSpeed(self):
        pass
    def setDir(self):
        pass
    def __updatePosition(self):
        pass

class Obstacle():
    def __init__(self):
        self.size = 0
        self.position = [0,0]
class Turn():
    def __init__(self):
        self.time = 0
        self.score = 0
        self.status = True
    def updateScore(self):
        pass
    def endTurn(self):
        pass


