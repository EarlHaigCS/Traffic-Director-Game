

#Tower Building Interface
# imports pygame modules
import pygame
from pygame.locals import *
import bbclasses


def TowerBuilding(colour):

    if colour == 'b' :
        tower = bbclasses.BlueTower(0)
    elif colour == 'r':
        tower = bbclasses.RedTower(0)
    elif colour == 'g':
        tower = bbclasses.GreenTower(0)
    elif colour == 'y':
        tower = bbclasses.YellowTower(0)

    game = bbclasses.TowerGame()

    blockslanded = []

    pygame.init() # initializes the pygame module
    #Set-up the main display window and the background
    size = (640, 480)  # size is set to a tuple representing standard for standard flash games
    screen = pygame.display.set_mode(size)  # Surface screen is set
    pygame.display.set_caption("Building Blox")  # Title bar caption is set
    img = pygame.image.load(tower.getBottomimg()).convert_alpha()  # loads the image for a tower block to img
    wire = pygame.image.load("images/Tower/wire.png").convert_alpha()  # loads the image for the swinging wire to wire
    cable = pygame.image.load("images/Tower/cable.png").convert_alpha()  # loads the image for cable fir top and bottom blocks

    # loads the image for the skyline background to background
    background = pygame.image.load("images/Tower/sky.png").convert()

    yposition = -2880.0  # float, vertical position to display the background. Initialized to show base of background
    wirebasex = 210.0     # constant float, initial horizontal position for wire. Future positions are based on this
    wirebasey = -150.0    # constant float, initial vertical position for wire. Future positions are based on this
    wirex = 0.0  # float, horizontal distance in addition to wirebasex
    wirey = 0.0  #float, vertical distance in addition to wirebasey
    wireyinc = 2.0  # represents the amount added to wirey every frame. Changes signs every time 0 degrees is passed
    cablex = 0.0
    cabley = 0.0

    screen.blit(background, (0, yposition))
    degrees = -20  # integer, degree at which surface objects are rotated; Counterclockwise is positive

    # Initial rotation of tower block and wire
    rotImg = pygame.transform.rotate(img,0)
    rotImg2 = pygame.transform.rotate(wire,degrees)

    # blockx: float, horizontal position of tower block surface. Calculated every frame based on position of the wire.
    blockx=float(wirex+wirebasex - (rotImg.get_width()/2))
    # blockx: float, vertical position of tower block surface. Calculated every frame based on position of the wire.
    blocky=float(wirey + wirebasey + rotImg2.get_height()- float((rotImg.get_height()/2)))
    blockoffset = 35.0

    screen.blit(rotImg2,(float(wirex + wirebasex), float(wirey + wirebasey)))
    screen.blit(rotImg, (blockx, blocky))

    clock = pygame.time.Clock() # Clock initialized to control frame rate
    keep_going = True 	        # boolean, controls whether the game loop continues

    #block/wire swinging variables
    increment = 1  # integer, represents the change in degrees each frame. changes signs when degrees reaches max or min
    dividevar = 20.0  # float, represents 'a' of the quadratic equation to calculate wirex. changes when degrees passes 0
    addition = 0  # float, represents 'b' of the quadratic equation to calculate wirex. changes when degrees passes 0

    #block falling variables
    haveblock = True  # boolean, True - block is swining, False - block is falling
    fallxisset = False  # boolean, flag that allows certain variables to be set only once after blocks starts falling
    falltime = 0  # integer, stores the number of frames passed after block starts falling
    oldwirex = 0.0  # integer, stores the horizontal position of block in previous frame

    blitblock = True  # used to prevent new block from being displayed at position previous block landed
    backgroundinc = img.get_height()

    passedlastblock = False
    # Game loop
    while keep_going:

        clock.tick(32) # sets frame rate at 32 fps

        #Handle  events in the frame
        for ev in pygame.event.get():
            if ev.type == QUIT:  # happens when the window is closed
                keep_going = False

            elif ev.type == KEYDOWN: # if it was a keyboard press
                if ev.key == K_DOWN:    # when down arror key is pressed
                    haveblock = False
                    '''if yposition <= -64:
                        yposition += 64'''
            elif ev.type == MOUSEBUTTONDOWN: # if the mouse was clicked
                haveblock = False  # treats as if down key was pressed
            else:
                pass  # does nothing for all other input events






        if img.get_height()- backgroundinc > 10:
            backgroundinc += 10
            yposition += 10
        elif img.get_height()- backgroundinc < 10:
            backgroundinc = img.get_height()
            yposition += (img.get_height()- backgroundinc)






        if len(blockslanded) < tower.getMaxLevel():
            degrees += increment # increments degrees to rotate images
            #rotates wire image
            rotImg2 = pygame.transform.rotate(wire,degrees)

            # updates oldwirex in case tower block needs to fall
            oldwirex = wirex

            wirey += wireyinc # increments the vertical position of the wire image

            # horizontal position of wire image is calculated using 2 different quadratic equations
            # when degrees is positive, wirex = 1/20 wirey^2
            # when degrees is negative, wirex = 1/40 wirey^2 + 120
            wirex = float(float((wirey*wirey)/dividevar)+addition)

            # Processes when degrees passes 0
            if degrees == 0:
                wireyinc *= -1  # vertical increments change signs
                # changes value of 'a' and 'b' to represent different quadratic function ax^2 + b
                if dividevar == -40:
                    dividevar = 20
                    addition = 0
                else:
                    dividevar = -40
                    addition = 120

            # changes the sign degrees is incremented to change direction of rotation
            if degrees == 20 or degrees == -20:
                increment *= -1

            # cable position
            if len(blockslanded) == 0 or len(blockslanded) == (tower.getMaxLevel() - 1):
                # movement for cable
                if wireyinc > 0:
                    cablex=float(wirex+wirebasex - float((cable.get_width()/2))) + 8.0
                else:
                    cablex=float(wirex+wirebasex + rotImg2.get_width() - float((cable.get_width()/2)))-12.0
                cabley=float(wirey + wirebasey + rotImg2.get_height())-5.0



            if haveblock == True: # if block is swinging on wire

                if len(blockslanded) == 0 or len(blockslanded) == (tower.getMaxLevel() - 1):  # first or last block
                    # movement for block
                    blockx = cablex +  float(cable.get_width()/2.0) - float(rotImg.get_width()/2.0)
                    blocky= cabley + rotImg.get_height() - blockoffset

                else:
                    #rotates block image according to the degrees of the swinging wire
                    rotImg = pygame.transform.rotate(img,degrees)

                    #calculates the position block needs to be placed based on position of the wire. Different calculation
                    #methods for horizontal position are used depending on whether the degree is negative or positive
                    if wireyinc > 0:
                        blockx=float(wirex+wirebasex - float((rotImg.get_width()/2)))+6
                    else:
                        blockx=float(wirex+wirebasex + rotImg2.get_width() - float((rotImg.get_width()/2)))-14
                    blocky=float(wirey + wirebasey + rotImg2.get_height()- float((rotImg.get_height()/2)))

            else: # if there is no block on the wire (i.e. user drops the block)
                blockdiff = 100
                '''condition for the block to stop falling'''
                if len(blockslanded)==0:   # passed y coordinate of bottom
                    if blocky > 323:
                        blockdiff = (img.get_width()/2.0)
                        blocky = 323
                        passedlastblock = True
                elif blocky >= blockslanded[-1].getyPos() - img.get_height():  # passed last block

                    blockdiff = blockx - blockslanded[-1].getxPos()
                    if abs(blockdiff) <= (img.get_width()/2.0):  # touches the previous blockblock in some way
                        blocky = blockslanded[-1].getyPos() - img.get_height()
                        passedlastblock = True

                '''if landed correctly'''
                if passedlastblock == True:

                    # if the block does not rotate back to normal in time, forcefully changes back to upright 0 degrees
                    rotImg = pygame.transform.rotate(img,0)

                    '''Sway algorithm'''
                    if abs(blockdiff) < 5:
                        pass

                    newblock = bbclasses.Block(blockx, blocky, 0, img)
                    blockslanded.append(newblock)
                    print len(blockslanded)
                    blitblock = False

                    if len(blockslanded) == 1: #after first block
                        img = pygame.image.load(tower.getMidimg()).convert_alpha()  # loads the image for a tower block to img
                        wire = pygame.image.load("images/Tower/hookwire.png").convert_alpha()  # loads the image for the swinging wire to wire
                        rotImg = pygame.transform.rotate(img,degrees)

                    elif len(blockslanded) == (tower.getMaxLevel() - 1):
                        img = pygame.image.load(tower.getTopimg()).convert_alpha()  # loads the image for a tower block to img
                        wire = pygame.image.load("images/Tower/wire.png").convert_alpha()  # loads the image for the swinging wire to wire
                        rotImg = pygame.transform.rotate(img,0)
                        if tower.getMaxLevel() == 40:
                            blockoffset = 95.0
                    if tower.getMaxLevel() > len(blockslanded) and len(blockslanded) > 1:
                        backgroundinc = 0
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() + img.get_height())

                    haveblock = True  # changes boolean value so that a new block may be generated back on the wire
                    passedlastblock = False
                    fallxisset = False  # changes boolean value so that fallx may be reset
                    falltime = 0  # sets amount of frames after falling back to 0

                    '''touches previous block, but too much to the side'''

                else:
                    falltime += 1  # increase the number of frames after block started falling

                    if fallxisset == False: #only sets horizontal velocity once
                        fallx=float(float(wirex-oldwirex)/5.0)
                        fallxisset = True
                        #falldegrees allows for the rotation of block and of wire to be stored separately
                        if len(blockslanded) == 0 or len(blockslanded) == (tower.getMaxLevel() - 1):
                            falldegrees = 0
                        else:
                            falldegrees = degrees

                    if falldegrees != 0:
                        falldegrees += wireyinc/2  #rotates the block a little every frame until it is upright
                    rotImg = pygame.transform.rotate(img,falldegrees)

                    #New coordinates for block is calculated
                    blockx = blockx + fallx
                    fally = float(float(1) + float(falltime*(2)))  # quadratic function to imitate physics of free fall
                    blocky = blocky + fally

                    '''block completely misses'''
                    if len(blockslanded)>0:
                        if blocky > 480:
                            haveblock = True  # changes boolean value so that a new block may be generated back on the wire
                            passedlastblock = False
                            fallxisset = False  # changes boolean value so that fallx may be reset
                            falltime = 0  # sets amount of frames after falling back to 0

        #Update and refresh the display to end this frame
        screen.blit(background, (0, yposition)) #<-- 'blit' means to copy one Surface to another

        if len(blockslanded) > 5:
            for i in range(-6,0):
                screen.blit(blockslanded[i].getImg(), (blockslanded[i].getxPos(),blockslanded[i].getyPos()))
        elif len(blockslanded) > 0:
            for blk in blockslanded:
                screen.blit(blk.getImg(), (blk.getxPos(),blk.getyPos()))

        screen.blit(rotImg2,(float(wirex+wirebasex), float(wirey+wirebasey)))
        if len(blockslanded) == 0 or len(blockslanded) >= (tower.getMaxLevel() - 1):
            screen.blit(cable, (cablex,cabley))
        if blitblock == True:
            screen.blit(rotImg, (blockx, blocky))
        elif haveblock == True:
            blitblock = True
<<<<<<< HEAD
        pygame.display.flip() #<-- refresh the display


=======
        pygame.display.flip() #<-- refresh the display
>>>>>>> FETCH_HEAD
