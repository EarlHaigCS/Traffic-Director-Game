"""
Coded by: Khashayar Pourdeilami
Pygame is the game engine used to make this game.
"""
import pygame
from pygame.locals import *
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
        # player's initial position is at the center
        self.position = [450, 300]
        # bounds are used to detect collisions.
        self.bounds = Rect(self.position[0], self.position[1], 25, 25)

        self.direction = "N"
    """
    Pre: The score must be inputted
    Post: To update the user high score if the score was bigger than the previous high score.
    Purpose: To set the user high score.
    """
    def setHighScore(self, score):

        if score > self.highScore: # the current turn score was bigger than the high score, set it as the high score.
            self.highScore = score

    """
    Pre: -
    Post: updates the bounds rectangle for the player.
    Purpose: to update the position of the player's collision detectors.
    """
    def updateBounds(self):
        self.bounds = Rect(self.position[0], self.position[1], 25, 25) # update the bounds of the player as it moves.

class City():

    """
    Pre: the size and population must be inputted
    Post: sets the size and population attributes to the inputted ones.
    Purpose: to set up the city.
    """
    def __init__(self, size, population):

        self.size = size

        self.population = population
    """
    Pre: -
    Post: Increases the population by 1
    Purpose: To avoid 0 population that results in 0 score.
    """
    def increasePopulation(self):

        self.population = self.population + 1

class Car():
    """
    Pre: -
    Post: Initializes the car object in terms of spped, direction, bounds and type.
    Purpose: to set up the cars.
    """
    def __init__(self):

        self.speed = 0 # the default speed for the cars

        self.direction = "N" # the default direction for the cars

        self.position = [randint(0, 900), randint(0, 600)] # randomly place the car

        self.bounds = Rect(self.position[0], self.position[1], 36, 50) # bounds used to detect collisions.

        self.setSpeed() # randomly assign a speed

        self.setDir() # randomly set the direction

        self.type = randint(3,6) # used to include different types of cars.

        if self.type in [1,2]: # if the car type was big
            self.bounds = Rect(self.position[0], self.position[1], 110, 42) # set new bounds to match the car size.
    """
    Pre: -
    Post: sets a new random speed to the car
    Purpose: to change the car's speed
    """
    def setSpeed(self):
        # random used to randomly assign a speed to the cars.
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
        """
        A series of if and elif statements to hold the cars in the screen and randomly assign a direction to them.
        """
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

        if turnTime > 1: # cars start moving after 1 second.
            """
            A series of if and elif statements used to update the position of the car based on the car's direction and speed.
            Also it updates the car's bounds based on their direction and position and type.
            """
            if self.direction == "N":

                self.position[1] = self.position[1] - self.speed # move the car

                self.bounds = Rect(self.position[0], self.position[1], 36, 50) #update bounds

                if self.type in [1,2]: # if it is a big car
                    self.bounds = Rect(self.position[0], self.position[1], 42, 110) #update bounds

            elif self.direction == "E":

                self.position[0] = self.position[0] - self.speed # move the car

                self.bounds = Rect(self.position[0], self.position[1], 50, 36) #update bounds

                if self.type in [1,2]: # if it is a big car
                    self.bounds = Rect(self.position[0], self.position[1], 110, 42) #update bounds

            elif self.direction == "S":

                self.position[1] = self.position[1] + self.speed # move the car

                self.bounds = Rect(self.position[0], self.position[1], 36, 50) #update bounds

                if self.type in [1,2]: # if it is a big car
                    self.bounds = Rect(self.position[0], self.position[1], 42, 110) #update bounds

            elif self.direction == "W":

                self.position[0] = self.position[0] + self.speed # move the car

                self.bounds = Rect(self.position[0], self.position[1], 50, 36) #update bounds

                if self.type in [1,2]: # if it is a big car

                    self.bounds = Rect(self.position[0], self.position[1], 110, 42) #update bounds



class Obstacle():
    """
    Pre: the size must be inputted
    Post: initializes the obstacle based on the size inputted.
    Purpose: to set up the obstacles.
    """
    def __init__(self, size):

        self.size = size
        """
        A series of if and elif statements to place the obstacles on the map.
        """
        if self.size == 1: # if it is a building

            self.position = [100, 250] #obstacle position

        elif self.size == 2: # if it is a building
            self.position = [500, 150] #obstacle position

        elif self.size == 3: # if it is a building
            self.position = [500, 50] #obstacle position

        elif self.size == 4: # if it is a star
            self.position = [randint(0, 900), randint(0, 600)] # randomly place it on a map

        elif self.size == 5: # if it is a building
            self.position = [100, 400] #obstacle position

        elif self.size == 6: # if it is a building
            self.position = [500, 250] #obstacle position

        elif self.size == 7: # if it is a building
            self.position = [100, 50]#obstacle position

        self.bounds = Rect(self.position[0] , self.position[1], 100, 100) #set the bounds to detect collisions.

        if self.size == 4:
            self.bounds = Rect(self.position[0] , self.position[1], 50, 50) # set the bounds for the stars


class Turn():
    """
    Pre: -
    Post: initializes the turn instance.
    Purpose: to set up the current turn.
    """
    def __init__(self):

        self.time = 0 # time is initially zero.

        self.score = 0 # score is initially zero.

        self.status = True # The main loop will run until turn.status is true
    """
    Pre: the city object must be inputted.
    Post: to update the turn score based on the time and city population.
    Purpose: to calculated the turn score.
    """
    def updateScore(self, city):

        self.score = round(city.population * self.time,1) # updates the current turn's score based on time and city's population.
    """
    Pre: -
    Post: sets the turn status to false.
    Purpose: to end the turn.
    """
    def endTurn(self):

        self.status = False # ends the main loop of the game.


