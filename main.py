
import pygame
from random import randint
from pygame.locals import *
from TrafficDirector import *
scriptDir = os.path.dirname(__file__)
pygame.init()
screen = pygame.display.set_mode((900,600))
image = pygame.image.load(os.path.join(scriptDir, "img/menu.png"))
screen.blit(image, (0,0))
pygame.display.set_caption('Traffic Director')
clock = pygame.time.Clock()
running = True
frame_count = 0

while running:
    clock.tick(30)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False
        elif ev.type == MOUSEBUTTONDOWN:
            trafficDirector = AvoidingCars()
            trafficDirector.run()
    pygame.display.flip()