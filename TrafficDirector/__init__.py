"""
Coded by: Khashayar Pourdeilami
Yaml library is used to parse yaml files. (pyyaml)
Pygame is the game engine used to make this game.
"""

import pygame
from pygame.locals import *
from classes import *
from menu import *
import os
from math import *
import time
import yaml
import webbrowser
scriptDir = os.path.dirname(__file__)
class TrafficDirector():

    """
    Pre: The TrafficDirector() class must be defined
    Post: Runs the game by calling the runMainLoop() function. When the process is done, it returns nothings to exit.
    Purpose: To start the 'Traffic Director' game.
    """
    def run(self):

        """
        Initializing pygame
        """

        width = 900 # The width of the game window

        height = 600 # The height of the game window


        """
        Pre: The run() method must be called.
        Post: Initializes the pygame, draws the necessary menus for the TrafficDirector game to the screen, sets up the map and handles the user's inputs.
        Purpose: To run the main loop of the game.
        """

        def runMainLoop():

            """
            Pre: The obstacles list and the cars list must be inputted
            Post: Returns 2 if the user is hit by a car, returns 3 if the user is trying to go out of the screen and returns 1
            if the user can't move because of an obstacle and returns 0 if the user can move freely. Also it returns 4 if the user catches a star.
            Purpose: To determine where the user can move to.
            """
            """
            This function was originally a method for the player but as it is only dedicated to the runMainLoop function it is
            encapsulated under the runMainLoop function.
            """
            def canMove(player, obstacles, cars):

                screen = Rect(0 , 0, 900, 600) # the screen rectangle.
                # for every car in the cars list
                for car in cars:
                    if player.bounds.colliderect(car.bounds) or car.bounds.colliderect(player.bounds): # if the car hit the player
                        try: # check to see if it is a star or a car
                            if car.size == 4: # to detect if it is an obstacle 4
                                return 4 # return 4 if it was a star.
                        except: # if it was a car return 2
                            return 2

                for obstacle in obstacles: # for all obstacles
                    if player.bounds.colliderect(obstacle.bounds): # if the player is about to enter an obstacle return 1
                        return 1

                if not screen.contains(player.bounds): # if the player is out of the screen return 3
                    return 3
                return 0 # if everything is fine, return 0
            """
            Pre: The data must be defined and must contain the previous the shared_data.yaml contents.
            Post: updates the shared data between the games based on the accomplishments in the past turn.
            Purpose: To save the data to the database.
            """
            """
            This function is encapsulated under the runMainLoop function and is only accessible to the runMainLoop function.
            """
            def updateDatabase():
                # opening the shared_data.yaml file.
                with open(os.path.join(scriptDir, "../shared_data.yaml"), 'w') as shared_data:
                    # updating the high score with the new high score.
                    data["TrafficDirector"]["highScore"] = round(player.highScore, 0)
                    # increasing the multiplier based on the player's high score.
                    data["shared_data"]["multiplier"] = data["shared_data"]["multiplier"] + log10(abs(turn.score)) / 1000
                    #increasing the raw population of the city
                    data["shared_data"]["raw_population"] = data["shared_data"]["raw_population"] + turnStars

                    if turnStars == data["shared_data"]["size"]:

                        data["shared_data"]["raw_population"] = data["shared_data"]["raw_population"] * 2

                    # modifying the population of the city
                    data["shared_data"]["population"] = round(data["shared_data"]["raw_population"] * data["shared_data"]["multiplier"],0)


                    """
                    A set of if statements to determine the city size.

                     Although I could have used range and elif statements but because it is less likely for the population to be less than
                    6400 so using ranges uses more memory. For example if the the population is 7000, the elif statements would do 14
                    requests but using  if statements, only 7 requests will be made.

                    The citySize variable is used to generate the map.
                    """
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
                    # updating the city size in the database.
                    data["shared_data"]["size"] = citySize
                    # writing all the modified data to the database.
                    shared_data.write(yaml.dump(data=data))

            """
            Initializing the game
            """
            pygame.init() # Initializing the Pygame

            screen = pygame.display.set_mode((width, height)) # Setting up the game screen

            pygame.display.set_caption('Traffic Director') # Setting the caption of the window

            pygame.mouse.set_visible(1) # Making the mouse visible

            background = pygame.Surface(screen.get_size()) # Initializing the background.

            background = background.convert() # Support for alpha

            clock = pygame.time.Clock() # Initializing the pygame clock.
            # Saving the time that the game started. Although the Pygame clock is used for the main while loop but the
            # python built-in time module is more accurate for other purposes.
            startTime = time.time()

            # Opening the database as read-only
            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'r') as shared_data:
                # Storing all the data inside the database to the data variable.
                data = yaml.load(shared_data)

            player = Player() # Initializing the player class

            turn = Turn() # Initializing the turn variable as an instance of the Turn class.

            city = City(data["shared_data"]["size"], data["shared_data"]["population"]) # Initializing the city based on the population stored in the data variable and the city size/

            player.highScore = data["TrafficDirector"]["highScore"] #Loading the high score from the database to the player object.

            obstacles = [] # an empty list of obstacles.

            cars = [Car(), Car(), Car(), Car(), Car(), Car(), Car()] # The default list of cars.

            for k in range(1, city.size, 1): # For loop to increase the number of cars in the cars list based on city population.

                cars.append(Car()) # Appending a new car to the cars list.
                # adding new obstacles to the obstacle list based on the city size.
                # each obstacle will have a different position from the other.
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


            for criminals in range (1 , city.size + 1, 1):

                cars.append(Obstacle(4))

            turnStars = 0;
            mainMenu = Menu(["Play", " ", "Quit"]) # The main menu of the game with two quit and play options.

            mainMenu.drawMenu(player.highScore) # Drawing the main menu upon the start of the game

            pauseMenu = PauseMenu("Resume", "Quit") # Pause menu is the menu used to pause the game.
            # the pause menu options won't show up on the screen.
            gameOverMenu = GameOverMenu("") # the game over menu.

            gameOver = False # gameOver is set to false on the start of the game to avoid showing the gameOverMenu when it is not required.
            # loading the player's image to the playerImage variable.
            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))

            """
            The background music settings

            when the game is still on the mainMenu, the bg.wav music will be played.
            """
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/bg.wav"))
            pygame.mixer.music.play(-1) # repeats the music for an infinite number of times.
            """
            Start of the game's main loop.
            """
            while turn.status: # while the turn.status is true the loop will run.
                # setting the frame rate of the game to 30 FPS
                clock.tick(30)
                # calculating the time that the current turn have started.
                turn.time = time.time() - startTime
                """
                The event handlers. (it is used to handle the user inputs)
                """
                for event in pygame.event.get(): # for every event.

                    mainMenu.handleEvent(event) # the event handler method for the mainMenu()

                    # quit the game if quit  is pressed
                    if event.type == QUIT:
                        return # returns nothing
                        """
                        The plain return command is not the correct way of doing this but it is the most efficient way.
                        Basicly it ends the current function without effecting other processes.
                        """
                    # Pausing or resuming the game if the player pressed the esc button.
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        # if the pause menu is active, disable it and if it is disabled, enable it.
                        if pauseMenu.isActive():

                            pauseMenu.deactivate()

                        else:
                             pauseMenu.activate()

                    elif event.type == KEYDOWN and event.key == K_h and mainMenu.isActive():
                        webbrowser.open("https://drive.google.com/file/d/0ByDvzb7bEi3qdlJqbnpWbGtDU0U/edit?usp=sharing")
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

                    elif event.type == MOUSEBUTTONDOWN and mainMenu.isActive():
                        mousePosition = pygame.mouse.get_pos() # getting the position of the mouse.
                        # It is an other way around to get the position of the click.

                        if mousePosition[0] > 300 and  mousePosition[0] < 600:

                            if mousePosition[1] > 280 and mousePosition[1] < 350: # if the player clicked on the play button
                                # if the player hit play, the background music will be changed.
                                pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/traffic.wav"))
                                # play the music forever.
                                pygame.mixer.music.play(-1)
                                # deactivate the main menu
                                mainMenu.deactivate()
                                # deactivate the pause menu.
                                pauseMenu.deactivate()

                            elif mousePosition[1] > 370 and mousePosition[1] < 450: # if the player clicked on the quit button.

                                return # quit the game


                screen.blit(background, (0, 0)) # blit the background to the screen.

                if mainMenu.isActive(): # if the main menu is active, draw the main menu.
                    mainMenu.drawMenu(player.highScore)

                elif pauseMenu.isActive(): # if the game is paused, draw the pause menu.
                    pauseMenu.drawMenu(turn.score)

                # if none of the menus is active run the game.
                else:

                    """
                    The code for setting up the game screen
                    """
                    # setting the background color to #999
                    background.fill((153,153,153))
                    # calculate the current turn's score based on the new time.
                    turn.updateScore(city)
                    # pygame font settings
                    font=pygame.font.Font(None,30)
                    # initializing the score text
                    scoretext=font.render("Score: " + str(turn.score), 1,(255,255,255))
                    # printing the text on the screen
                    screen.blit(scoretext, (110, 15))
                    # initializing the star text
                    starText=font.render( "Win Points: "+ str(turnStars) + "  out of " + str(city.size), 1,(255,255,255))
                    # printing the text on the screen
                    screen.blit(starText, (300, 15))

                    if turnStars == city.size:
                        wonImage = pygame.image.load(os.path.join(scriptDir, "img/won.png"))
                        background.blit(wonImage, (0,0))

                    """
                    The code for generating the map

                    there is not much to generate, just the obstacles. The obstacles will be placed based on the obstacles list.
                    """
                    for obstacle in obstacles: # for every obstacle in the city.
                        # load the obstacle image based on the obstacle type.
                        if obstacle.size == 1:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))
                            obstacle.bounds = Rect(obstacle.position[0] ,obstacle.position[1], 110, 110) # set the bounds to detect collisions
                        elif obstacle.size == 2:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 3:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 5:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))
                            obstacle.bounds = Rect(obstacle.position[0] ,obstacle.position[1], 110, 110) # set the bounds to detect collisions

                        elif obstacle.size == 6:
                            image = pygame.image.load(os.path.join(scriptDir, "img/park.png"))

                        elif obstacle.size == 7:
                            image = pygame.image.load(os.path.join(scriptDir, "img/building2.png"))
                            obstacle.bounds = Rect(obstacle.position[0] ,obstacle.position[1], 110, 110) # set the bounds to detect collisions

                        # print the obstacle to the screen based on the obstacle's position.
                        background.blit(image, [obstacle.position[0], obstacle.position[1]])

                    """
                    The code for the moving cars
                    """
                    # to avoid cars  on the menus
                    if turn.time > -1:
                        for car in cars: # for all cars in the cars list do the following.
                            try: # to avoid crashing when the car is not a car. ( the Obstacle(4) might be in the cars list too.)
                                otherCars = [] # a copy of the cars list.
                                otherCars = cars # copying everything from cars into the otherCars list.
                                for anotherCar in otherCars: # for another car in the other cars.
                                    # if car and another car were about to collide
                                    if car.bounds.colliderect(anotherCar.bounds) and car.position != anotherCar.position:
                                        car.setDir() # change the direction of the car
                                        car.setSpeed() # change the speed of the car.
                                """
                                A series of if and elif statements to keep the moving cars in the screen.
                                """
                                if car.position[0] > 900:
                                    car.direction = "E"
                                elif car.position[0] < 0:
                                    car.direction = "W"
                                elif car.position[1] < 0:
                                    car.direction = "S"
                                elif car.position[1] > 600:
                                    car.direction = "N"
                                # for every obstacle in the obstacles list.
                                for obstacle in obstacles:
                                    if car.bounds.colliderect(obstacle.bounds): # if the car is about to hit an obstacle.
                                        car.setDir() # change the direction of the car.
                                        car.setSpeed() # change the speed of the car.


                                car.updatePosition(turn.time) # update the position of the car based on the car's speed and direction.
                                """
                                A series of if and elif statements to have different car types.
                                It is just a fancy feature and is abandoned for now, but it works and needs to be activated
                                in the Car() class.
                                """
                                if car.type in [1,2]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/bigCar.png"))

                                elif car.type in [3,4]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/car.png"))

                                elif car.type in [5,6]:
                                    carImage = pygame.image.load(os.path.join(scriptDir, "img/car.png"))
                                """
                                A series of if and elif statements to rotate the car based on it's direction.
                                """
                                if car.direction == "S":
                                    carImage = pygame.transform.rotate(carImage, 270)

                                elif car.direction == "N":
                                    carImage = pygame.transform.rotate(carImage, 90)

                                elif car.direction == "E":
                                    carImage = pygame.transform.rotate(carImage, 180)
                                # printing the car to the screen.
                                background.blit(carImage, car.position)

                            except AttributeError: # If it was an Obstacle(4)
                                #print the restricted area to the screen.
                                """
                                The car after here is referred to the Obstacle(4) in the cars list. For some reason
                                if I call it something else, the code for the obstacles break. This probably a Pygame glitch
                                because I have faced this issue with Pygame before.
                                """

                                image = pygame.image.load(os.path.join(scriptDir, "img/star.png"))
                                car.bounds = Rect(car.position[0] , car.position[1], 50, 50) # updating the bounds of the star.
                                background.blit(image, [car.position[0], car.position[1]]) # printing on the screen.



                    """
                    The code for the moving player
                    """
                    # The following lines are there two make the running animation possible.
                    if canMove(player ,obstacles, cars) == 0 or turn.time < 4: # if the player can freely move.

                        if int(turn.time*5) % 3 == 0: # mod 3 because there are three different running images.
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player-running-1.png"))
                        elif int(turn.time*5) % 3 == 1:
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player-running-2.png"))
                        else:
                            playerImage = pygame.image.load(os.path.join(scriptDir, "img/player.png"))

                        """
                        A set of if and elif statements to displace the player based on the player's direction.
                        Also they rotate the player to match it's direction and update the player's position based on it's direction.
                        """
                        if player.direction == "N":
                            if turn.time > 1:
                                player.position[1] = player.position[1] - 12
                            playerImage = pygame.transform.rotate(playerImage, 0)

                        elif player.direction == "W":
                            player.position[0] = player.position[0] - 12
                            playerImage = pygame.transform.rotate(playerImage, 90)

                        elif player.direction == "E":
                            player.position[0] = player.position[0] + 12
                            playerImage = pygame.transform.rotate(playerImage, 270)

                        elif player.direction == "S":
                            player.position[1] = player.position[1] + 12
                            playerImage = pygame.transform.rotate(playerImage, 180)

                    elif canMove(player ,obstacles, cars) == 1: # if the player can't move due to an obstacle.
                        """
                        take control over the player and don't let the user to hide in the buildings.
                        """
                        player.position = [player.position[0] + 5, player.position[1] + 5]
                    # if the player is about th exit the screen.
                    elif canMove(player ,obstacles, cars) == 3:
                        """
                        A set of if and elif statements to hold the player from exiting the screen.
                        """
                        if player.position[0] < 30:
                            player.position = [player.position[0] + 5, player.position[1]]
                            player.direction = "E"

                        elif player.position[0] > 870:
                            player.position = [player.position[0] - 5, player.position[1]]
                            player.direction = "W"

                        elif player.position[1] < 30:
                            player.position = [player.position[0], player.position[1] + 5]
                            player.direction = "S"

                        elif player.position[1] > 570:
                            player.position = [player.position[0], player.position[1] - 5]
                            player.direction = "N"

                    elif canMove(player ,obstacles, cars) == 4: # if the player catches a star

                        for car in cars: # remove the star from the screen
                            if car.bounds.colliderect(player.bounds):
                                cars.remove(car)
                        turnStars = turnStars + 1 # increase the number of stars by 1.

                    elif canMove(player ,obstacles, cars) == 2: # if the player has hit an obstacle 4 is hit by a car
                        if turn.time > 4:
                            pygame.mixer.music.load(os.path.join(scriptDir, "sound_tracks/car_crash.wav")) # play the game over sound once.

                            pygame.mixer.music.play(1) # play it the game over sound once.

                            turn.updateScore(city) # update the turn's score

                            player.setHighScore(turn.score) # set the high score for the player.

                            turn.endTurn() # end the current turn.

                            gameOver = True # the game is over now.

                    player.updateBounds() # update the boundaries of the player.
                    #activates the player shield for the first 4 seconds of the game.
                    if turn.time < 4:
                        if int(turn.time*5) % 2 == 0: # used to change the shield's color.
                            sheildImage = pygame.image.load(os.path.join(scriptDir, "img/circle_close_delete-48.png"))
                        else:
                            sheildImage = pygame.image.load(os.path.join(scriptDir, "img/circle_close_delete-48_2.png"))
                        background.blit(sheildImage, (player.position[0] - 13, player.position[1] - 12.5)) # printing the shiled to the screen.


                    background.blit(playerImage, player.position) # print the player to the screen.

                pygame.display.flip() # update the screen after each time the main loop is done.


            while gameOver: # if the game is over

                for event in pygame.event.get(): # an event handler for the game over menu.

                    # Starting the game over
                    if event.type == KEYDOWN and event.key == K_a: # if the player hit the a button restart the game.

                        updateDatabase() # update the database with the new information.

                        runMainLoop() # run the game again.
                        return # end the current function.

                    elif event.type == QUIT: # quit the game if the quit is pressed.
                        return # quit

                gameOverMenu.drawMenu(turn.score) # draw the game over menu.

                pygame.display.flip() # update the score.

        runMainLoop() # run the main loop.
        return # end the function when the main loop is over.

