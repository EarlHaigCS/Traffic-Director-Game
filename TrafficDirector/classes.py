"""
Coded by: Khashayar Pourdeilami
Pygame is the game engine used to make this game.
"""
import pygame
from pygame.locals import *
import ConfigParser
import os
from random import randint
scriptDir = os.path.dirname(__file__)

class Player():
    """
    Pre: -
    Post: The player bounds, position, direction and high score will be initialized.
    Purpose: To initialize the player.
    """
    def __init__(self):

        self.highScore = 0

        self.position = [450, 300]

        self.bounds = Rect(self.position[0], self.position[1], 25, 25)

        self.direction = "N"
    """
    Pre: The score must be inputted
    Post: To update the user high score if the score was bigger than the previous high score.
    Purpose: To set the user high score.
    """
    def setHighScore(self, score):

        if score > self.highScore:
            self.highScore = score
    """
    Pre: The obstacles list and the cars list must be inputted
    Post: Returns 2 if the user is hit by a car, returns 3 if the user is trying to go out of the screen and returns 1
    if the user can't move because of an obstacle and returns 0 if the user can move freely.
    Purpose: To determine where the user can move to.
    """
    def canMove(self, obstacles, cars):

        screen = Rect(0 , 0, 900, 600)

        for car in cars:
            if self.bounds.colliderect(car.bounds) or car.bounds.colliderect(self.bounds):
                try:
                    if car.status == True:
                        return 4
                except:
                    return 2

        for obstacle in obstacles:
            if self.bounds.colliderect(obstacle.bounds):
                return 1

        if not screen.contains(self.bounds):
            return 3
        return 0
    """
    Pre: -
    Post: updates the bounds rectangle for the player.
    Purpose: to update the position of the player's collision detectors.
    """
    def updateBounds(self):
        self.bounds = Rect(self.position[0], self.position[1], 25, 25)

class City():

    """
    Pre: the size and population must be inputted
    Post: sets the size and population attributes to the inputted ones.
    Purpose: to set up the city.
    """
    def __init__(self, size, population):

        self.size = size

        self.population = population

class Car():
    """
    Pre: -
    Post: Initializes the car object in terms of spped, direction, bounds and type.
    Purpose: to set up the cars.
    """
    def __init__(self):

        self.speed = 0

        self.direction = "N"

        self.position = [randint(0, 900), randint(0, 600)]

        self.bounds = Rect(self.position[0], self.position[1], 36, 50)

        self.setSpeed()

        self.setDir()

        self.type = randint(4,6)

        if self.type in [1,2]:
            self.bounds = Rect(self.position[0], self.position[1], 110, 42)
    """
    Pre: -
    Post: sets a new random speed to the car
    Purpose: to change the car's speed
    """
    def setSpeed(self):

        random = randint(1, 3)

        if random == 1:
            self.speed = 4

        elif randint == 2:
            self.speed = 8

        else:
            self.speed = 12

    """
    Pre: -
    Post: sets a new direction for the car based on the car's position and a random number.
    Purpose:
    """
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
    """
    Pre: -
    Post: updates the position of the car based on the car's direction and speed, also updates the car's bounds.
    Purpose: to update the car's position.
    """
    def updatePosition(self, turnTime):

        if turnTime > 1:

            if self.direction == "N":

                self.position[1] = self.position[1] - self.speed

                self.bounds = Rect(self.position[0], self.position[1], 36, 50)

                if self.type in [1,2]:
                    self.bounds = Rect(self.position[0], self.position[1], 42, 110)

            elif self.direction == "E":

                self.position[0] = self.position[0] - self.speed

                self.bounds = Rect(self.position[0], self.position[1], 50, 36)

                if self.type in [1,2]:
                    self.bounds = Rect(self.position[0], self.position[1], 110, 42)

            elif self.direction == "S":

                self.position[1] = self.position[1] + self.speed

                self.bounds = Rect(self.position[0], self.position[1], 36, 50)

                if self.type in [1,2]:
                    self.bounds = Rect(self.position[0], self.position[1], 42, 110)

            elif self.direction == "W":

                self.position[0] = self.position[0] + self.speed

                self.bounds = Rect(self.position[0], self.position[1], 50, 36)

                if self.type in [1,2]:

                    self.bounds = Rect(self.position[0], self.position[1], 110, 42)



class Obstacle():
    """
    Pre: the size must be inputted
    Post: initializes the obstacle based on the size inputted.
    Purpose: to set up the obstacles.
    """
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
    """
    Pre: -
    Post: initializes the turn instance.
    Purpose: to set up the current turn.
    """
    def __init__(self):

        self.time = 0

        self.score = 0

        self.status = True
    """
    Pre: the city object must be inputted.
    Post: to update the turn score based on the time and city population.
    Purpose: to calculated the turn score.
    """
    def updateScore(self, city):

        self.score = round(city.population * self.time,1)
    """
    Pre: -
    Post: sets the turn status to false.
    Purpose: to end the turn.
    """
    def endTurn(self):

        self.status = False


