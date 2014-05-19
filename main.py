"""
By: Khashayar Pourdeilami
Yaml library is used to parse yaml files. (pyyaml)
Pygame is the game engine used to make this game.
"""
import pygame
from random import randint
from pygame.locals import *
from TrafficDirector import *
from BuildingBlox import *
from ChooChooTrain import *
scriptDir = os.path.dirname(__file__)


"""
Pre: -
Post: To replace the content of the new_game_shared_data.yaml with the content of the shared_data.yaml file.
Purpose: To start a new game.
"""
def newGame():

    with open(os.path.join(scriptDir, "new_game_shared_data.yaml"), 'r') as new_shared_data: # open the new data file.

            new_data = yaml.load(new_shared_data) # copy the new data to the new_data variable.

    with open(os.path.join(scriptDir, "shared_data.yaml"), 'w') as shared_data: # open the shared data file

        shared_data.write(yaml.dump(data=new_data)) # replace the content with the content of the new_data



with open(os.path.join(scriptDir, "shared_data.yaml"), 'r') as shared_data: # open the shared data file.

    data = yaml.load(shared_data) # load all te data into the data variable.

pygame.init() #initializing the pygame.

screen = pygame.display.set_mode((900,600)) # setting the screen size.

pygame.display.set_caption('City Manager') # setting the caption of the window

clock = pygame.time.Clock() # pygame clock needs to be initialized

running = True # Used to control the main loop.

welcomeMenu = True # welcome menu shows up automatically after launch.

gameMenu = False

while running: # the main loop of the game

    clock.tick(30) # setting the FPS to 30.

    with open(os.path.join(scriptDir, "shared_data.yaml"), 'r') as shared_data: # opening the shared data file.

        data = yaml.load(shared_data) #loading the content to the data variable.

    for ev in pygame.event.get(): # event handler of the menu

        if ev.type == QUIT: # if the user wants to quit the game.

            running = False # stop the main loop

        elif ev.type == MOUSEBUTTONDOWN and gameMenu: # if the game menu is active and the user clicked somewhere.

            mousePosition = pygame.mouse.get_pos() # getting the position of the click.

            # The back button
            if mousePosition[0] > 850 and  mousePosition[0] < 900:

                if mousePosition[1] > 0 and mousePosition[1] < 100:

                    gameMenu = False
                    welcomeMenu= True

            if mousePosition[1] > 400 and mousePosition[1] < 580:

                # Starting traffic director  game

                if mousePosition[0] > 670 and  mousePosition[0] < 850:

                    trafficDirector = TrafficDirector()
                    trafficDirector.run()

                # Starting building Blox game
                if mousePosition[0] > 470 and  mousePosition[0] < 650:

                    buildingBlox = BuildingBlox()
                    buildingBlox.run()
                    screen = pygame.display.set_mode((900,600))  # Surface screen is set
                    pygame.display.set_caption("City Manager")  # Title bar caption is set

                # Starting  choo choo train game
                if mousePosition[0] > 260 and  mousePosition[0] < 440:
                    chooChooTrain = ChooChooTrain()
                    chooChooTrain.run()
                    screen = pygame.display.set_mode((900,600))  # Surface screen is set
                    pygame.display.set_caption("City Manager")  # Title bar caption is set


        elif ev.type == MOUSEBUTTONDOWN: # if the user clicked on the screen and the welcome menu was active.

            mousePosition = pygame.mouse.get_pos() # getting the mouse position

            if mousePosition[0] > 329 and  mousePosition[0] < 571:
                # activating the game menu and loading the game from memory.
                if mousePosition[1] < 100 and mousePosition[1] > 60:

                    gameMenu = True
                    welcomeMenu= False
                # starting a new game and activating the game menu.
                elif mousePosition[1] < 200 and mousePosition[1] > 160:

                    newGame()
                    gameMenu = True
                    welcomeMenu= False
                # if the user pressed the quit
                elif mousePosition[1] < 300 and mousePosition[1] > 260:

                    running = False # stop the game.

    # drawing the welcome menu on the screen.
    if welcomeMenu:
        image = pygame.image.load(os.path.join(scriptDir, "img/menu.png")).convert_alpha()
        screen.blit(image, (0,0))
    # drawing the game menu on the screen.
    elif gameMenu:

        image = pygame.image.load(os.path.join(scriptDir, "img/status.png"))

        screen.blit(image, (0,0))

        cityTypeText = ""
        """
        A Bunch of if statements to set the city type text.

        Although I could have used range and elif statements but because it is less likely for the population to be less than
        6400 so using ranges uses more memory. For example if the the population is 7000, the elif statements would do 14
        requests but using  if statements, only 12 requests will be made.
        """
        if data["shared_data"]["population"] > 0 :
             cityTypeText =  "settlement"

        if data["shared_data"]["population"] > 200:
            cityTypeText =  "village"

        if data["shared_data"]["population"] > 400:
            cityTypeText =  "small town"

        if data["shared_data"]["population"] > 800:
           cityTypeText =  " town"

        if data["shared_data"]["population"] > 1600:
            cityTypeText =  "small city"

        if data["shared_data"]["population"] > 3200:
            cityTypeText =  "mid-sized city"

        if data["shared_data"]["population"] > 6400:
            cityTypeText =  "large city"

        if data["shared_data"]["population"] > 12800:
            cityTypeText =  "capital"

        if data["shared_data"]["population"] > 25600:
            cityTypeText =  "metropolitan"

        if data["shared_data"]["population"] > 51200:
            cityTypeText =  "world-class city"

        if data["shared_data"]["population"] > 102400:
            cityTypeText =  "city-state"

        if data["shared_data"]["population"] > 180000:
            cityTypeText =  "galactic supercenter"

        """
        Printing texts  to the screen
        """

        font=pygame.font.Font(None,40)
        # Printing the city related info to the screen.
        population  = font.render(str(int(data["shared_data"]["population"])) + " people live in your " + cityTypeText ,  1,(153,153,153))
        # setting the text position to be center.
        textpos = population.get_rect()
        # setting the text position to be center.
        textpos.centerx = screen.get_rect().centerx
        # determining the text's y position.
        textpos.centery = 45
        # printing to screen.
        screen.blit(population, textpos)

        font=pygame.font.Font(None,30)
        # Printing "Increase your city's population by playing the mini games below." to the screen
        info  = font.render("Increase your city's population by playing the mini games below.",  1,(170,170,170))
        # setting the text position to be center.
        textpos = info.get_rect()
        # setting the text position to be center.
        textpos.centerx = screen.get_rect().centerx
        #determining the text's y position.
        textpos.centery = 80
        # printing to the screen
        screen.blit(info, textpos)
        # Printing high score for traffic directing game
        font=pygame.font.Font(None,18)

        info  = font.render("High Score: " + str(data["TrafficDirector"]["highScore"]),  1,(255,255,255))

        screen.blit(info, (680, 560))
        # Printing high score for Building Blox game
        info  = font.render("High Score: " + str(data["BuildingBlox"]["highScore"]),  1,(255,255,255))
        # Printing high score for  Choo Choo Train game.
        screen.blit(info, (480, 560))

        info  = font.render("High Score: " + str(data["ChooChooTrain"]["highScore"]),  1,(255,255,255))

        screen.blit(info, (270, 560))


    else:
        running = False # end the game
    pygame.display.flip() # update the screen.
