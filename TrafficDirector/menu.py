"""
External Library taken from: https://github.com/BradStevenson/Pygame-Menu
"""
import pygame
from pygame.locals import *
import os
scriptDir = os.path.dirname(__file__)
class MenuItem (pygame.font.Font):

    def __init__(self, text, position, fontSize=36, antialias=1, color=(255, 255, 255), background=None):
        pygame.font.Font.__init__(self, None, fontSize)
        self.text = text
        if background == None:
            self.textSurface = self.render(self.text, antialias, (255, 255, 255))
        else:
            self.textSurface = self.render(self.text, antialias, (255, 255, 255), background)

        self.position = self.textSurface.get_rect(centerx=position[0], centery=position[1])
    def get_pos(self):
        return self.position
    def get_text(self):
        return self.text
    def get_surface(self):
        return self.textSurface


class Menu():

    MENUCLICKEDEVENT = USEREVENT + 1

    def __init__(self, menuEntries, menuCenter=None):
        '''
        The constructer uses a list of string for the menu entries,
        which need  to be created
        and a menu center if non is defined, the center of the screen is used
        '''
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        image = pygame.image.load(os.path.join(scriptDir, "img/menu.png"))
        self.background.blit(image, (0,0))
        self.active = False

        if pygame.font:
            fontSize = 50
            fontSpace = 4
            # loads the standard font with a size of 36 pixels
            # font = pygame.font.Font(None, fontSize)

            # calculate the height and startpoint of the menu
            # leave a space between each menu entry
            menuHeight = (fontSize + fontSpace) * len(menuEntries)
            startY = self.background.get_height() / 2 - menuHeight / 2

            # listOfTextPositions=list()
            self.menuEntries = list()
            for menuEntry in menuEntries:
                centerX = self.background.get_width() / 2
                centerY = startY + fontSize + fontSpace + 50
                newEnty = MenuItem(menuEntry, (centerX, centerY))
                self.menuEntries.append(newEnty)
                self.background.blit(newEnty.get_surface(), newEnty.get_pos())
                startY = startY + fontSize + fontSpace - 10



    def drawMenu(self, highScore):
        self.active = True
        screen = pygame.display.get_surface()

        screen.blit(self.background, (0, 0))
        font=pygame.font.Font(None,20)
        scoreText = font.render("High Score: " + str(highScore), 1,(255,255,255))
        helpText = font.render("* Press H for help", 1,(255,255,255))
        screen.blit(self.background, (0, 0))
        screen.blit(scoreText, (5, 580))
        screen.blit(helpText, (400, 470))

    def isActive(self):
        return self.active
    def activate(self,):
        self.active = True
    def deactivate(self):
        self.active = False
    def handleEvent(self, event):
        # only send the event if menu is active
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            # initiate with menu Item 0
            curItem = 0
            # get x and y of the current event
            eventX = event.pos[0]
            eventY = event.pos[1]
            # for each text position
            for menuItem in self.menuEntries:
                textPos = menuItem.get_pos()
                # check if current event is in the text area
                if eventX > textPos.left and eventX < textPos.right \
                and eventY > textPos.top and eventY < textPos.bottom:
                    # if so fire new event, which states which menu item was clicked
                    menuEvent = pygame.event.Event(self.MENUCLICKEDEVENT, item=curItem, text=menuItem.get_text())
                    pygame.event.post(menuEvent)
                curItem = curItem + 1



class PauseMenu(Menu):

    def __init__(self, menuEntries, menuCenter=None):
        '''
        The constructer uses a list of string for the menu entries,
        which need  to be created
        and a menu center if non is defined, the center of the screen is used
        '''
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        image = pygame.image.load(os.path.join(scriptDir, "img/pauseMenu.png"))
        self.background.blit(image, (0,0))
        self.active = False

    def drawMenu(self, score):
        self.active = True
        screen = pygame.display.get_surface()

        # render text
        font=pygame.font.Font(None,30)
        scoretext=font.render(str(score), 1,(255,255,255))
        screen.blit(self.background, (0, 0))
        screen.blit(scoretext, (110, 15))

class GameOverMenu(Menu):

    def __init__(self, menuEntries, menuCenter=None):
        '''
        The constructer uses a list of string for the menu entries,
        which need  to be created
        and a menu center if non is defined, the center of the screen is used
        '''
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        image = pygame.image.load(os.path.join(scriptDir, "img/gameOverMenu.png"))
        self.background.blit(image, (0,0))
        self.active = False

    def drawMenu(self, score):
        self.active = True
        screen = pygame.display.get_surface()

        # render text
        font=pygame.font.Font(None,30)
        scoretext=font.render(str(score), 1,(255,255,255))
        screen.blit(self.background, (0, 0))
        screen.blit(scoretext, (110, 15))


