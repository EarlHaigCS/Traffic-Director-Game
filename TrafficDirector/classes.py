import pygame
from pygame.locals import *
import ConfigParser
import os
from random import randint
scriptDir = os.path.dirname(__file__)

class Player():

    def __init__(self):

        self.highScore = 0

        self.position = [450, 300]

        self.bounds = Rect(self.position[0], self.position[1], 25, 25)

        self.direction = "N"

    def setHighScore(self, score):

        if score > self.highScore:
            self.highScore = score

    def canMove(self, obstacles, cars):

        screen = Rect(0 , 0, 900, 600)

        for car in cars:
            if self.bounds.colliderect(car.bounds) or car.bounds.colliderect(self.bounds):
                return 2

        for obstacle in obstacles:
            if self.bounds.colliderect(obstacle.bounds):
                return 1

        if not screen.contains(self.bounds):
            return 3
        return 0

    def updateBounds(self):
        self.bounds = Rect(self.position[0], self.position[1], 25, 25)

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

        self.position = [randint(0, 900), randint(0, 600)]

        self.bounds = Rect(self.position[0], self.position[1], 36, 50)

        self.setSpeed()

        self.setDir()

        self.type = randint(3,6)

        if self.type in [1,2]:
            self.bounds = Rect(self.position[0], self.position[1], 146, 56)

    def setSpeed(self):

        random = randint(1, 2)

        if random == 1:
            self.speed = 2

        else:
            self.speed = 5

    def setDir(self):

        random = randint(1, 4)

        if random == 1 and self.position[1] > 0:
            self.direction = "N"

        elif random == 2 and self.position[0] > 0:
            self.direction = "E"

        elif random == 3 and self.position[1] < 800:
            self.direction = "S"

        elif random == 4 and self.position[0] < 800:
            self.direction = "W"

    def updatePosition(self):

        if self.direction == "N":

            self.position[1] = self.position[1] - self.speed

            self.bounds = Rect(self.position[0], self.position[1], 36, 50)

            if self.type in [1,2]:
                self.bounds = Rect(self.position[0], self.position[1], 56, 146)

        elif self.direction == "E":

            self.position[0] = self.position[0] - self.speed

            self.bounds = Rect(self.position[0], self.position[1], 50, 36)

            if self.type in [1,2]:
                self.bounds = Rect(self.position[0], self.position[1], 146, 56)

        elif self.direction == "S":

            self.position[1] = self.position[1] + self.speed

            self.bounds = Rect(self.position[0], self.position[1], 36, 50)

            if self.type in [1,2]:
                self.bounds = Rect(self.position[0], self.position[1], 56, 146)

        elif self.direction == "W":

            self.position[0] = self.position[0] + self.speed

            self.bounds = Rect(self.position[0], self.position[1], 50, 36)

            if self.type in [1,2]:

                self.bounds = Rect(self.position[0], self.position[1], 146, 56)



class Obstacle():

    def __init__(self, size):

        self.size = size

        if self.size == 1:

            self.position = [100, 250]

        elif self.size == 2:
            self.position = [500, 150]

        elif self.size == 3:
            self.position = [500, 50]

        elif self.size == 4:
            self.position = [randint(0, 900), randint(0, 600)]

        elif self.size == 5:
            self.position = [100, 400]

        elif self.size == 6:
            self.position = [500, 250]

        elif self.size == 7:
            self.position = [100, 50]

        self.bounds = Rect(self.position[0] , self.position[1], 100, 100)

        if self.size == 4:
            self.bounds = Rect(self.position[0] , self.position[1], 50, 50)

        self.status = True

class Turn():
    def __init__(self):

        self.time = 0

        self.score = 0

        self.status = True

    def updateScore(self, city):

        self.score = city.population * self.time

    def endTurn(self):

        self.status = False


