import pygame
from pygame.locals import *
from classes import *
from menu import *
import os

class AvoidingCars():
    """
    Pre:
    Post:
    Purpose:
    """
    def __init__(self):
        self.status = False
    """
    Pre:
    Post:
    Purpose:
    """
    def run(self):

        width = 600
        height = 600

        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Avoiding Cars Game')
        pygame.mouse.set_visible(1)
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()



        # draw background
        screen.blit(background, (0, 0))
        pygame.display.flip()


        mainMenu = Menu(["Play", " ", "Quit"])
        mainMenu.drawMenu()



        while 1:
            clock.tick(60)

            for event in pygame.event.get():
                mainMenu.handleEvent(event)
                # quit the game if escape is pressed
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    mainMenu.activate()
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text == "Quit":
                        return
                    elif event.item == 0:
                        isGameActive = True
                        mainMenu.deactivate()
            screen.blit(background, (0, 0))
            if mainMenu.isActive():
                mainMenu.drawMenu()
            else:
                background.fill((229, 233, 236))


            pygame.display.flip()
    """
    Pre:
    Post:
    Purpose:
    """
    def end(self):
        self.status = False

    """
    Pre:
    Post:
    Purpose:
    """
    def restart(self):
        pass
