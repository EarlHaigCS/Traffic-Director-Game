
import pygame
from random import randint
from pygame.locals import *
from TrafficDirector import *
from BuildingBlox import *
from ChooChooTrain import *


scriptDir = os.path.dirname(__file__)

def loadGame(type):

    if type == "existing":
        pass
    elif type == "new": # starting a new game and discarding the one in the memory!

        with open(os.path.join(scriptDir, "new_game_shared_data.yaml"), 'r') as new_shared_data:

            new_data = yaml.load(new_shared_data)

    with open(os.path.join(scriptDir, "shared_data.yaml"), 'w') as shared_data:

        shared_data.write(yaml.dump(data=new_data))

def newGame():

    loadGame("new")

def saveGame():

    pass



with open(os.path.join(scriptDir, "shared_data.yaml"), 'r') as shared_data:

    data = yaml.load(shared_data)

pygame.init()

screen = pygame.display.set_mode((900,600))

pygame.display.set_caption('Traffic Director')

clock = pygame.time.Clock()

running = True

welcomeMenu = True

gameMenu = False

while running:

    clock.tick(30)

    with open(os.path.join(scriptDir, "shared_data.yaml"), 'r') as shared_data:

        data = yaml.load(shared_data)

    for ev in pygame.event.get():

        if ev.type == QUIT:

            running = False

        elif ev.type == MOUSEBUTTONDOWN and gameMenu:

            mousePosition = pygame.mouse.get_pos()

            # The back button
            if mousePosition[0] > 850 and  mousePosition[0] < 900:

                if mousePosition[1] > 0 and mousePosition[1] < 100:

                    gameMenu = False
                    welcomeMenu= True

            if mousePosition[1] > 400 and mousePosition[1] < 580:
                # Starting traffic director  game
                if mousePosition[0] > 670 and  mousePosition[0] < 850:

                    trafficDirector = AvoidingCars()
                    trafficDirector.run()
                # Starting building blox game
                if mousePosition[0] > 470 and  mousePosition[0] < 650:

                    buildingBlox = BuildingBlox()
                    buildingBlox.run()
                # Starting  choo choo train game
                if mousePosition[0] > 260 and  mousePosition[0] < 440:

                    chooChooTrain = ChooChooTrain()
                    chooChooTrain.run()

            #saving the game
            if mousePosition[0] > 10 and mousePosition[0] < 120:

                if mousePosition[1] > 10 and mousePosition[1] < 50:

                    saveGame()

        elif ev.type == MOUSEBUTTONDOWN:

            mousePosition = pygame.mouse.get_pos()

            if mousePosition[0] > 329 and  mousePosition[0] < 571:

                if mousePosition[1] < 100 and mousePosition[1] > 60:

                    gameMenu = True
                    welcomeMenu= False

                elif mousePosition[1] < 200 and mousePosition[1] > 160:

                    newGame()
                    gameMenu = True
                    welcomeMenu= False

                elif mousePosition[1] < 300 and mousePosition[1] > 260:

                    loadGame("existing")

                elif mousePosition[1] < 400 and mousePosition[1] > 360:

                    running = False

    if welcomeMenu:

        image = pygame.image.load(os.path.join(scriptDir, "img/menu.png"))

        screen.blit(image, (0,0))

    elif gameMenu:

        image = pygame.image.load(os.path.join(scriptDir, "img/status.png"))

        screen.blit(image, (0,0))

        cityTypeText = ""

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

        textpos = population.get_rect()

        textpos.centerx = screen.get_rect().centerx

        textpos.centery = 45

        screen.blit(population, textpos)

        font=pygame.font.Font(None,30)
        # Printing "Increase your city's population by playing the mini games below." to the screen
        info  = font.render("Increase your city's population by playing the mini games below.",  1,(170,170,170))

        textpos = info.get_rect()

        textpos.centerx = screen.get_rect().centerx

        textpos.centery = 80

        screen.blit(info, textpos)
        # Printing high score for traffic directing game
        font=pygame.font.Font(None,18)

        info  = font.render("High Score: " + str(data["TrafficDirector"]["highScore"]),  1,(255,255,255))

        screen.blit(info, (680, 560))

        info  = font.render("High Score: " + str(data["BuildingBlox"]["highScore"]),  1,(255,255,255))

        screen.blit(info, (480, 560))

        info  = font.render("High Score: " + str(data["ChooChooTrain"]["highScore"]),  1,(255,255,255))

        screen.blit(info, (270, 560))


    else:
        running = False
    pygame.display.flip()
