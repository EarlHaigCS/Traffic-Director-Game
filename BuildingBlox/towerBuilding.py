#Tower Building Interface
# imports pygame modules
import pygame
from pygame.locals import *
import bbclasses
import math

def TowerBuilding(colour):
    repeat = True

    while repeat:
        if colour == 'b' :
            tower = bbclasses.BlueTower(0)
        elif colour == 'r':
            tower = bbclasses.RedTower(0)
        elif colour == 'g':
            tower = bbclasses.GreenTower(0)
        elif colour == 'y':
            tower = bbclasses.YellowTower(0)

        pygame.init()  # initializes the pygame module

        '''Fonts and Text'''
        pygame.font.init()
        myfont = pygame.font.Font("fonts/jtwya.ttf", 19)
        myfont.set_bold(True)
        myfont2 = pygame.font.Font("fonts/jtwya.ttf", 28)
        myfont2.set_bold(True)
        resfont = pygame.font.SysFont("monospace", 32, True)

        againlabel = myfont.render("Close window to", 1, (0, 0, 0))
        exitlabel = myfont.render("play again!", 1, (0, 0, 0))


        #Set-up the main display window and the background
        size = (640, 480)  # size is set to a tuple representing standard for standard flash games
        screen = pygame.display.set_mode(size)  # Surface screen is set

        '''Load images'''
        pygame.display.set_caption("Building Blox")  # Title bar caption is set
        img = pygame.image.load(tower.getBottomimg()).convert_alpha()  # loads the image for a tower block to img
        wire = pygame.image.load("images/Tower/wire.png").convert_alpha()  # loads the image for the swinging wire to wire
        cable = pygame.image.load("images/Tower/cable.png").convert_alpha()  # loads the image for cable fir top and bottom blocks

        heart = pygame.image.load("images/Tower/heart.png").convert_alpha()
        frame = pygame.image.load("images/Tower/frame.png").convert_alpha()
        floorind = pygame.image.load("images/Tower/floorindicator.png").convert_alpha()
        resicon = pygame.image.load("images/Tower/residenticon.png").convert_alpha()

        # loads the image for the skyline background to background
        background = pygame.image.load("images/Tower/sky.png").convert()

        yposition = -2880.0  # float, vertical position to display the background. Initialized to show base of background
        wirebasex = 210.0     # constant float, initial horizontal position for wire. Future positions are based on this
        wirebasey = -150.0    # constant float, initial vertical position for wire. Future positions are based on this
        wirex = 0.0  # float, horizontal distance in addition to wirebasex
        wirey = 0.0  # float, vertical distance in addition to wirebasey
        wireyinc = 2.0  # represents the amount added to wirey every frame. Changes signs every time 0 degrees is passed
        cablex = 0.0
        cabley = 0.0

        screen.blit(background, (0, yposition))
        degrees = -20  # integer, degree at which surface objects are rotated; Counterclockwise is positive

        # Initial rotation of tower block and wire
        rotImg = pygame.transform.rotate(img,0)
        rotImg2 = pygame.transform.rotate(wire,degrees)

        # blockx: float, horizontal position of block surface. Calculated every frame based on position of the wire.
        blockx=float(wirex+wirebasex - (rotImg.get_width()/2))
        # blockx: float, vertical position of tower block surface. Calculated every frame based on position of the wire.
        blocky=float(wirey + wirebasey + rotImg2.get_height()- float((rotImg.get_height()/2)))
        blockoffset = 35.0

        screen.blit(rotImg2,(float(wirex + wirebasex), float(wirey + wirebasey)))
        screen.blit(rotImg, (blockx, blocky))

        clock = pygame.time.Clock() # Clock initialized to control frame rate
        keep_going = True 	        # boolean, controls whether the game loop continues

        blockslanded = []

        lives = 3
        imperfect = 0  # integer, number of imperfectly landed blocks, used to calculate sway effect
        sway = 0.0
        swaypos = 0.0
        swayinc = sway/16.0
        waitframe = 10

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

        blitframe = False  # Boolean variable, prevents the block from being displayed immediately after img change
        tilt = False  # Boolean variable, used to initiate the tilt animation after a block successfully lands
        eligible = True  # Boolean variable, used to ensure that position of block (hit or miss) is only evaluated once
        tumble = False  # Boolean variable to initiate tumbling of previous block due to imperfect landing
        shiftdown = True  # Boolean variable, determines whether the background should shift up or down
        perfect = False  # Boolean variable, set to True when the block lands perfectly
        framecount = 0  # integer, counts the number of frames for long lasting events
        bonusblocks = []  # list, stores the bonus points for each block in a bonus streak
        secondsleft = 0
        residents = 0
        resinc = 0

        # Game loop
        while keep_going:

            floorlabel = myfont.render(str(len(blockslanded))+"/"+str(tower.getMaxLevel()), 1, (255, 255, 255))

            clock.tick(32) # sets frame rate at 32 fps

            #Handle  events in the frame
            for ev in pygame.event.get():
                if ev.type == QUIT:  # happens when the window is closed
                    keep_going = False

                elif ev.type == KEYDOWN: # if it was a keyboard press
                    if ev.key == K_DOWN:    # when down arror key is pressed
                        haveblock = False
                elif ev.type == MOUSEBUTTONDOWN: # if the mouse was clicked
                    haveblock = False  # treats as if down key was pressed
                else:
                    pass  # does nothing for all other input events

            '''Shifting the background gradually'''

            if img.get_height() - backgroundinc > 10:
                backgroundinc += 10.0
                if shiftdown:
                    yposition += 10.0
                    for blk in blockslanded:
                        blk.setyPos(blk.getyPos() + 10.0)
                else:
                    yposition -= 10.0
                    for blk in blockslanded:
                        blk.setyPos(blk.getyPos() - 10.0)
            elif img.get_height() - backgroundinc < 10:

                if shiftdown:
                    yposition += (img.get_height() - backgroundinc)
                    for blk in blockslanded:
                        blk.setyPos(blk.getyPos() + img.get_height()-backgroundinc)
                else:
                    yposition -= (img.get_height() - backgroundinc)
                    for blk in blockslanded:
                        blk.setyPos(blk.getyPos() - (img.get_height()-backgroundinc))
                backgroundinc = img.get_height()
                shiftdown = True

            '''Tilting effect'''
            if tilt:
                if abs(tiltdeg)<=0.5:
                    tiltdeg = 0
                    blockslanded[-1].setyPos(blockslanded[-2].getyPos()-img.get_height())
                    tilt = False
                elif tiltdeg>0:
                    tiltdeg -= 0.5
                    blockslanded[-1].setyPos(blockslanded[-1].getyPos() + 0.35)
                elif tiltdeg<0:
                    tiltdeg += 0.5
                    blockslanded[-1].setyPos(blockslanded[-1].getyPos() + 0.35)
                #if len(blockslanded) == tower.getMaxLevel()-1:
                blockslanded[-1].setImg(pygame.transform.rotate(pygame.image.load(tower.getMidimg()).convert_alpha(),tiltdeg))

            '''Perfect landing effect'''
            if perfect:
                framecount -= 1
                secondsleft = framecount/32
                if framecount == 0:
                    perfect = False

            '''Main loop for tower game, continues until game is finished'''
            if len(blockslanded) < tower.getMaxLevel() and lives > 0:
                degrees += increment # increments degrees to rotate images
                #rotates wire image
                rotImg2 = pygame.transform.rotate(wire, degrees)

                '''Swaying effect x position change'''
                if waitframe == 10:
                    swaypos += swayinc
                    if abs(swaypos) >= sway:
                        waitframe -= 1
                        swayinc *= -1
                elif waitframe == 0:
                    waitframe = 10
                else:
                    waitframe -= 1


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

                if haveblock:  # if block is swinging on wire

                    if len(blockslanded) == 0 or len(blockslanded) == (tower.getMaxLevel() - 1):  # first or last block
                        # movement for block
                        if len(blockslanded) == (tower.getMaxLevel() - 1):
                            rotImg = pygame.transform.rotate(img, 0)
                        blockx = cablex + float(cable.get_width()/2.0) - float(rotImg.get_width()/2.0)
                        blocky = cabley + rotImg.get_height() - blockoffset

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

                    '''if landed correctly'''
                    if passedlastblock:

                        # if the block does not rotate back to normal in time, forcefully changes back to upright 0 degrees
                        rotImg = pygame.transform.rotate(img,0)
                        '''Perfect Landing'''
                        if abs(blockdiff) < 6:
                            perfect = True
                            bonusblocks = []
                            framecount = 160  # 5 seconds
                            resinc = (len(blockslanded)/20)+5
                        else:
                            imperfect +=1
                            resinc = (len(blockslanded)/20)+2
                            if imperfect%3 == 0:
                                sway += 5.0
                            if swayinc > 0:
                                swayinc = sway/16.0
                            else:
                                swayinc = -(sway/16.0)
                        residents += resinc

                        if len(blockslanded) % 5 == 0 and imperfect > 0:
                            sway += 5.0

                        '''Operations for bonus streak'''
                        if perfect:
                            bonusblocks.append(len(bonusblocks)*secondsleft)

                        newblock = bbclasses.Block(blockx-swaypos, blocky, resinc, img)
                        blockslanded.append(newblock)

                        haveblock = True  # changes boolean value so that a new block may be generated back on the wire
                        passedlastblock = False
                        fallxisset = False  # changes boolean value so that fallx may be reset
                        falltime = 0  # sets amount of frames after falling back to 0
                        eligible = True

                        if tower.getMaxLevel() > len(blockslanded) > 1:
                            backgroundinc = 0

                            '''Landing tilt animation'''
                            if abs(blockdiff) >= 6:
                                tiltdeg = blockdiff * -0.5
                                tiltimg = pygame.transform.rotate(blockslanded[-1].getImg(),tiltdeg)
                                blockslanded[-1].setImg(tiltimg)
                                blockslanded[-1].setyPos(blockslanded[-1].getyPos()-(tiltimg.get_height()-img.get_height()-(abs(blockdiff)*math.sin(abs(tiltdeg)*3.1416/180.0))))
                                tilt = True

                        if len(blockslanded) == 1:  # after first block
                            img = pygame.image.load(tower.getMidimg()).convert_alpha()  # loads the image for a tower block to img
                            wire = pygame.image.load("images/Tower/hookwire.png").convert_alpha()  # loads the image for the swinging wire to wire
                            rotImg = pygame.transform.rotate(img, degrees)
                            blitblock = False

                        elif len(blockslanded) == (tower.getMaxLevel() - 1):
                            img = pygame.image.load(tower.getTopimg()).convert_alpha()  # loads the image for a tower block to img
                            wire = pygame.image.load("images/Tower/wire.png").convert_alpha()  # loads the image for the swinging wire to wire
                            rotImg = pygame.transform.rotate(img, 0)
                            if tower.getMaxLevel() == 40:
                                blockoffset = 95.0
                            blitblock = False
                    else:
                        falltime += 1  # increase the number of frames after block started falling
                        if fallxisset == False:  # only sets horizontal velocity once
                            if tumble:
                                if blockdiff > 0:
                                    tumbleinc = -1.0
                                else:
                                    tumbleinc = 1.0
                                fallx = 3.5
                                falldegrees = 0
                            else:
                                tumbleinc = 1.0
                                fallx=float(float(wirex-oldwirex)/5.0)
                                #falldegrees allows for the rotation of block and of wire to be stored separately
                                if len(blockslanded) == 0 or len(blockslanded) == (tower.getMaxLevel() - 1):
                                    falldegrees = 0
                                else:
                                    falldegrees = degrees
                            fallxisset = True
                        if tumble:
                            falldegrees += 10
                            fally = float(1.0 + float(falltime*1.5))  # quadratic function to imitate physics of free fall
                            blockx += (fallx*tumbleinc*-1)
                        else:
                            fally = float(1.0 + float(falltime*2))  # quadratic function to imitate physics of free fall
                            if falldegrees != 0:
                                falldegrees += wireyinc/2  # rotates the block a little every frame until it is upright
                            blockx += fallx

                        rotImg = pygame.transform.rotate(img, falldegrees*tumbleinc)

                        #New coordinates for block is calculated


                        blocky = blocky + fally


                        if eligible == True:  # Prevents block to be evaluated (hit/miss) more than once
                            blockdiff = 100
                            '''condition for the block to stop falling'''
                            if len(blockslanded)==0:   # passed y coordinate of bottom
                                if blocky > 323:
                                    blockdiff = (img.get_width()/2.0)
                                    blocky = 323
                                    passedlastblock = True
                            elif blocky >= blockslanded[-1].getyPos() - img.get_height():  # passed last block
                                blockdiff = blockx - (blockslanded[-1].getxPos()+swaypos)
                                if abs(blockdiff) <= (img.get_width()/2.0):  # touches the previous blockblock in some way
                                    blocky = blockslanded[-1].getyPos() - img.get_height()
                                    passedlastblock = True
                                elif abs(blockdiff) < img.get_width():  # Will knock off previous block
                                    tumble = True
                                    '''needs to start new parabola'''
                                    fallxisset = False  # changes boolean value so that fallx may be reset
                                    falltime = 0  # sets amount of frames after falling back to 0
                                    tempimg = blockslanded[-1].getImg()
                                eligible = False
                        else:
                            '''Tumbling animation when current block knocks out previous block'''
                            if tumble:
                                if tower.getMaxLevel()-1 > len(blockslanded) > 1:
                                    blockslanded[-1].setImg(pygame.transform.rotate(tempimg, falldegrees))
                                    blockslanded[-1].setxPos(blockslanded[-1].getxPos()-fallx)
                                    blockslanded[-1].setyPos(blocky+img.get_height())
                            if blocky > 480:
                                lives -= 1
                                haveblock = True  # changes boolean value so that a new block may be generated back on the wire
                                passedlastblock = False
                                fallxisset = False  # changes boolean value so that fallx may be reset
                                falltime = 0  # sets amount of frames after falling back to 0
                                eligible = True
                                if 1 < len(blockslanded) < (tower.getMaxLevel()-1) and tumble:
                                    resinc = -1*blockslanded[-1].getRes()
                                    residents += resinc
                                    blockslanded.pop(-1)  # delete previous block
                                    backgroundinc = 0
                                    shiftdown = False
                                    tumbleinc = 1.0
                                tumble = False  # reset the tumble variable for the next block drop


            else:
                blitframe = True
            #Update and refresh the display to end this frame

            '''Background'''
            screen.blit(background, (0, yposition))

            '''Displays blocks previously landed as a tower'''
            if len(blockslanded) > 5:
                for i in range(-6, 0):
                    screen.blit(blockslanded[i].getImg(), (blockslanded[i].getxPos()+swaypos, blockslanded[i].getyPos()))
            elif len(blockslanded) > 0:
                for blk in blockslanded:
                    screen.blit(blk.getImg(), (blk.getxPos()+swaypos, blk.getyPos()))

            '''Wire or Hookwire / '''
            screen.blit(rotImg2, (float(wirex+wirebasex), float(wirey+wirebasey)))

            '''Cable /\ '''
            if len(blockslanded) == 0 or len(blockslanded) >= (tower.getMaxLevel() - 1):
                screen.blit(cable, (cablex, cabley))

            '''Will not blit first frame after img changes'''
            if blitblock:
                screen.blit(rotImg, (blockx, blocky))
            elif haveblock:
                blitblock = True

            '''Floors constructed'''
            screen.blit(floorind, (30, 360))
            screen.blit(floorlabel, (41, 416))

            '''Lives left heart display <3 '''
            if lives > 0:
                screen.blit(heart, (130, 415))
                if lives > 1:
                    screen.blit(heart, (170, 415))
                    if lives > 2:
                        screen.blit(heart, (210, 415))

            '''Residents'''
            if resinc != 0:
                if resinc > 0:
                    resincdisplay = resfont.render("+"+str(resinc), 1, (0, 255, 0))
                else:
                    resincdisplay = resfont.render(str(resinc), 1, (255, 0, 0))
                screen.blit(resincdisplay, (70, 50))
            screen.blit(resicon, (450, 410))
            totalres = "0"*(5-len(str(residents)))+str(residents)
            totresdis = myfont2.render(totalres, 1, (255, 255, 255))
            screen.blit(totresdis, (475, 405))

            '''Bonus streak bar and glow'''
            if perfect:
                pass

            '''Ending screen'''
            if blitframe:
                screen.blit(frame, (170, 100))
                screen.blit(againlabel, (220, 160))
                screen.blit(exitlabel, (230, 185))

            pygame.display.flip()  # Refresh the display