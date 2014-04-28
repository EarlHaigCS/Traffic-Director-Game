import pygame
from pygame.locals import *
from classes import *
from menu import *
import os
from math import *
import sqlite3
import sys
scriptDir = os.path.dirname(__file__)
import yaml
class AvoidingCars():

    """
    Pre:
    Post:
    Purpose:
    """
    def run(self):
        """
        Initializing pygame
        """

        width = 900

        height = 600

        pygame.init()

        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Traffic Director')

        pygame.mouse.set_visible(1)

        background = pygame.Surface(screen.get_size())

        background = background.convert()

        clock = pygame.time.Clock()

        def runMainLoop():
            """
            Initializing the game
            """

            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'rw') as shared_data:

                data = yaml.load(shared_data)

            player = Player()

            turn = Turn()

            city = City(data["shared_data"]["size"], data["shared_data"]["population"])

            player.highScore = data["TrafficDirector"]["highScore"]

            obstacles = []

            cars = [Car(), Car(), Car(), Car(), Car(), Car(), Car()]

            for k in range(1, city.size, 1):

                cars.append(Car())

                if k == 2:
                    obstacles.append(Obstacle(1))

                elif k == 3:
                    obstacles.append(Obstacle(3))

                elif k == 4:
                    obstacles.append(Obstacle(2))

                elif k == 5:
                    obstacles.append(Obstacle(7))

                elif k == 6:
                    obstacles.append(Obstacle(5))

                elif k == 7:
                    obstacles.append(Obstacle(6))

            if data["shared_data"]["anti_crime"] < city.size:

                for criminals in range (1 , city.size - data["shared_data"]["anti_crime"], 1):

                    cars.append(Obstacle(4))

            mainMenu = Menu(["Play", " ", "Quit"])

            mainMenu.drawMenu(player.highScore)

            pauseMenu = PauseMenu("Resume", "Quit")

            gameOverMenu = GameOverMenu("")

            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))

            """
            The background music settings
            """
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/bg.wav"))
            pygame.mixer.music.play(-1)
            """
            Start of the game's main loop
            """
            while turn.status:

                clock.tick(30)

                turn.time = pygame.time.get_ticks() / 1000
                """
                The event handlers
                """
                for event in pygame.event.get():

                    mainMenu.handleEvent(event)

                    # quit the game if escape is pressed
                    if event.type == QUIT:
                        return
                    # Pausing the game
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:

                        if pauseMenu.isActive():

                            pauseMenu.deactivate()

                        else:
                             pauseMenu.activate()

                    # Reseting the game
                    elif event.type == KEYDOWN and event.key == K_a:
                        runMainLoop()

                    # Moving UP
                    elif event.type == KEYDOWN and event.key == K_UP:
                        player.direction = "N"

                    # Moving Left
                    elif event.type == KEYDOWN and event.key == K_LEFT:
                        player.direction = "W"

                    # Moving Down
                    elif event.type == KEYDOWN and event.key == K_DOWN:
                        player.direction = "S"

                    # Moving Right
                    elif event.type == KEYDOWN and event.key == K_RIGHT:
                        player.direction = "E"
                    # Handling the Menu Input

                    elif event.type == mainMenu.MENUCLICKEDEVENT:
                        if event.text == "Quit":
                            return

                        elif event.item == 0:
                            pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/traffic.wav"))
                            pygame.mixer.music.play(-1)
                            mainMenu.deactivate()
                            pauseMenu.deactivate()

                screen.blit(background, (0, 0))

                if mainMenu.isActive():
                    mainMenu.drawMenu(player.highScore)

                elif pauseMenu.isActive():
                    turn.updateScore(city)
                    pauseMenu.drawMenu(turn.score)

                elif gameOverMenu.isActive():
                    gameOverMenu.drawMenu(turn.score)

                else:
                    background.fill((153,153,153))
                    """
                    The code for generating the map
                    """
                    for obstacle in obstacles:
                        if obstacle.size == 1:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))

                        elif obstacle.size == 2:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 3:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 5:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))

                        elif obstacle.size == 6:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 7:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))

                        background.blit(image, [obstacle.position[0], obstacle.position[1]])

                    """
                    The code for the moving cars
                    """
                    if turn.time > 0:
                        for car in cars:
                            try:
                                otherCars = []
                                otherCars = cars
                                for anotherCar in otherCars:
                                    if car.bounds.colliderect(anotherCar.bounds) and car.position != anotherCar.position:
                                        car.setDir()
                                        car.setSpeed()

                                if car.position[0] > 900:
                                    car.direction = "E"
                                elif car.position[0] < 0:
                                    car.direction = "W"
                                elif car.position[1] < 0:
                                    car.direction = "S"
                                elif car.position[1] > 600:
                                    car.direction = "N"

                                for obstacle in obstacles:
                                    if car.bounds.colliderect(obstacle.bounds):
                                        car.setDir()


                                car.updatePosition(turn.time)

                                if car.type in [1,2]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/bigCar.png"))

                                elif car.type in [3,4]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/car.png"))

                                elif car.type in [5,6]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/car.png"))

                                if car.direction == "S":
                                    carImage = pygame.transform.rotate(carImage, 270)

                                elif car.direction == "N":
                                    carImage = pygame.transform.rotate(carImage, 90)

                                elif car.direction == "E":
                                    carImage = pygame.transform.rotate(carImage, 180)

                                background.blit(carImage, car.position)
                            except AttributeError:

                                image = pygame.image.load(os.path.join(scriptDir, "img/vampire.png"))
                                car.position = [car.position[1], car.position[0]]
                                car.bounds = Rect(car.position[0] , car.position[1], 50, 50)
                                background.blit(image, [car.position[0], car.position[1]])



                    """
                    The code for the moving player
                    """
                    if player.canMove(obstacles, cars) == 0:

                        if player.direction == "N":
                            player.position[1] = player.position[1] - 10
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))
                            playerImage = pygame.transform.rotate(playerImage, 0)

                        if player.direction == "W":
                            player.position[0] = player.position[0] - 10
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))
                            playerImage = pygame.transform.rotate(playerImage, 90)

                        if player.direction == "E":
                            player.position[0] = player.position[0] + 10
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))
                            playerImage = pygame.transform.rotate(playerImage, 270)

                        if player.direction == "S":
                            player.position[1] = player.position[1] + 10
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))
                            playerImage = pygame.transform.rotate(playerImage, 180)

                    elif player.canMove(obstacles, cars) == 1:
                        player.position = [player.position[0] + 5, player.position[1] + 5]

                    elif player.canMove(obstacles, cars) == 3:

                        if player.position[0] < 30:
                            player.position = [player.position[0] + 5, player.position[1]]

                        elif player.position[0] > 870:
                            player.position = [player.position[0] - 5, player.position[1]]

                        elif player.position[1] < 30:
                            player.position = [player.position[0], player.position[1] + 5]

                        elif player.position[1] > 570:
                            player.position = [player.position[0], player.position[1] - 5]

                    elif player.canMove(obstacles, cars) == 2:

                        pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/car_crash.wav"))

                        pygame.mixer.music.play(1)

                        turn.updateScore(city)

                        player.setHighScore(turn.score)

                        turn.endTurn()

                    player.updateBounds()

                    background.blit(playerImage, player.position)

                pygame.display.flip()

            """
            Saving the updates to the database
            """

            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'w') as shared_data:

                data["TrafficDirector"]["highScore"] = round(player.highScore, 0)

                data["shared_data"]["population"] = round(data["shared_data"]["raw_population"] * data["shared_data"]["multiplier"],0)

                data["shared_data"]["multiplier"] = data["shared_data"]["multiplier"] + log10(turn.score) / 100

                if data["shared_data"]["population"] > 0 :
                    citySize = 1

                if data["shared_data"]["population"] > 200:
                    citySize = 2

                if data["shared_data"]["population"] > 400:
                    citySize = 3

                if data["shared_data"]["population"] > 800:
                    citySize = 4

                if data["shared_data"]["population"] > 1600:
                    citySize = 5

                if data["shared_data"]["population"] > 3200:
                    citySize = 6

                if data["shared_data"]["population"] > 6400:
                    citySize = 7

                if data["shared_data"]["population"] > 12800:
                    citySize = 8

                if data["shared_data"]["population"] > 25600:
                    citySize = 9

                if data["shared_data"]["population"] > 51200:
                    citySize = 10

                if data["shared_data"]["population"] > 102400:
                    citySize = 11

                if data["shared_data"]["population"] > 180000:
                    citySize = 12

                data["shared_data"]["size"] = citySize

                shared_data.write(yaml.dump(data=data,))

            while True:

                for event in pygame.event.get():

                    # Starting the game over
                    if event.type == KEYDOWN and event.key == K_a:
                        runMainLoop()

                    elif event.type == QUIT:
                        return

                gameOverMenu.drawMenu(turn.score)

                pygame.display.flip()

        runMainLoop()

    """
    Pre:
    Post:
    Purpose:
    """
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)