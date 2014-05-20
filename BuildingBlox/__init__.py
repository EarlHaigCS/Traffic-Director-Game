#Tower Building Interface
# imports pygame modules
import pygame
from pygame.locals import *
import classes
import math
import os
import time
import yaml
import webbrowser
scriptDir = os.path.dirname(__file__)
class BuildingBlox():
    def run(self):

        # Opening the database as read-only
        with open(os.path.join(scriptDir, "../shared_data.yaml"), 'r') as shared_data:
            # Storing all the data inside the database to the data variable.
            data = yaml.load(shared_data)

        pygame.init()  # initializes the pygame module
        pygame.font.init()
        clock = pygame.time.Clock() # Clock initialized to control frame rate
        #Set-up the main display window and the background
        size = (640, 480)  # size is set to a tuple representing standard for standard flash games
        screen = pygame.display.set_mode(size)  # Surface screen is set
        pygame.display.set_caption("Building Blox")  # Title bar caption is set

        '''Music'''
        music = pygame.mixer.music.load(os.path.join(scriptDir, "sound/music.wav"))
        pygame.mixer.music.play(-1)
        musicplaying = True

        residents = 0

        """
        Pre: The data must be defined and must contain the previous the shared_data.yaml contents.
        Post: updates the shared data between the games based on the accomplishments in the past turn.
        Purpose: To save the data to the database.
        """
        def updateDatabase():
            global residents
            # opening the shared_data.yaml file.
            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'w') as shared_data:

                if residents > data["BuildingBlox"]["highScore"]:
                    # updating the high score with the new high score.
                    data["BuildingBlox"]["highScore"] = residents
                #increasing the raw population of the city
                data["shared_data"]["raw_population"] = data["shared_data"]["raw_population"] + residents
                # modifying the population of the city
                data["shared_data"]["population"] = round(data["shared_data"]["raw_population"] * data["shared_data"]["multiplier"],0)

                """
                A set of if statements to determine the city size.

                 Although I could have used range and elif statements but because it is less likely for the population to be less than
                6400 so using ranges uses more memory. For example if the the population is 7000, the elif statements would do 14
                requests but using  if statements, only 7 requests will be made.

                The citySize variable is used to generate the map.
                """
                totolpop = data["shared_data"]["population"]
                if totolpop > 180000 :
                    citySize = 12

                elif totolpop > 102400:
                    citySize = 11

                elif totolpop > 51200:
                    citySize = 10

                elif totolpop > 25600:
                    citySize = 9

                elif totolpop > 12800:
                    citySize = 8

                elif totolpop > 6400:
                    citySize = 7

                elif totolpop > 3200:
                    citySize = 6

                elif totolpop > 1600:
                    citySize = 5

                elif totolpop > 800:
                    citySize = 4

                elif totolpop > 400:
                    citySize = 3

                elif totolpop > 200:
                    citySize = 2

                elif totolpop > 0:
                    citySize = 1
                # updating the city size in the database.
                data["shared_data"]["size"] = citySize

                # writing all the modified data to the database.
                shared_data.write(yaml.dump(data=data))

        def mainMenu():
            '''Fonts and Text'''
            myfont = pygame.font.Font(os.path.join(scriptDir,"fonts/hollow.ttf"), 96)
            myfont.set_bold(False)
            myfont2 = pygame.font.Font(os.path.join(scriptDir,"fonts/hollow.ttf"), 56)
            myfont2.set_bold(False)
            myfont3 = pygame.font.Font(os.path.join(scriptDir,"fonts/hollow.ttf"), 28)
            myfont3.set_bold(False)
            title = myfont.render("Building Blox", 1, (0, 0, 0))
            playgame = myfont2.render("Play Game!", 1, (0, 0, 0))
            instructions = myfont2.render("Instructions", 1, (0, 0, 0))
            gamemenu = myfont2.render("Game Suite", 1, (0, 0, 0))
            hslabel = myfont3.render("High Score: "+str(data["BuildingBlox"]["highScore"])+" Residents", 1, (0, 0, 0))
            difficulty = myfont2.render("Choose Difficulty:", 1, (0, 0, 0))
            bluechoice = myfont2.render("Apartment (10 Floors)", 1, (0, 0, 0))
            redchoice = myfont2.render("Condo (20 Floors)", 1, (0, 0, 0))
            greenchoice = myfont2.render("Complex (30 Floors)", 1, (0, 0, 0))
            yellowchoice = myfont2.render("Skyscraper (40 Floors)", 1, (0, 0, 0))
            backtext = myfont2.render("Back", 1, (0, 0, 0))

            background = pygame.image.load(os.path.join(scriptDir,"images/Menu/mainmenubk.png")).convert_alpha()
            musicbutton = pygame.image.load(os.path.join(scriptDir,"images/Tower/musicbutton.png")).convert_alpha()
            blue = pygame.image.load(os.path.join(scriptDir,"images/Menu/blueComp.png")).convert_alpha()
            red = pygame.image.load(os.path.join(scriptDir,"images/Menu/redComp.png")).convert_alpha()
            green = pygame.image.load(os.path.join(scriptDir,"images/Menu/greenComp.png")).convert_alpha()
            yellow = pygame.image.load(os.path.join(scriptDir,"images/Menu/yellowComp.png")).convert_alpha()

            global residents
            global musicplaying
            musicplaying = True

            keep_going = True
            menu = True
            chooselevel = False
            instructionsscreen = False
            instrslide = 0

            while keep_going:
                #Handle  events in the frame
                for ev in pygame.event.get():
                    if ev.type == QUIT:  # happens when the window is closed
                        keep_going = False
                    elif ev.type == MOUSEBUTTONDOWN: # if the mouse was clicked
                        mousepos = pygame.mouse.get_pos()
                        mousex = mousepos[0]
                        mousey = mousepos[1]
                        '''Music button'''

                        if 10<mousex<81 and 10<mousey<35:

                            if musicplaying:
                                pygame.mixer.music.pause()
                                musicplaying = False
                            else:
                                pygame.mixer.music.unpause()
                                musicplaying = True

                            '''Main Menu Button'''
                        elif menu:
                            '''Play Game'''
                            if 230<mousex<230+playgame.get_width() and 180<mousey<236:
                                chooselevel = True
                                menu = False

                                '''Instructions'''
                            elif 230<mousex<230+instructions.get_width() and 260<mousey<316:
                                instructionsscreen = True
                                instrslide += 1
                                menu = False

                                '''Game Suite'''
                            elif 230<mousex<230+gamemenu.get_width() and 340<mousey<396:
                                keep_going=False
                                pygame.mixer.music.stop()

                        elif chooselevel:
                            '''10 Floors'''
                            if 70<mousex<130+bluechoice.get_width() and 110<mousey<166:
                                buildTower('b')

                                '''20'''
                            elif 70<mousex<130+redchoice.get_width() and 180<mousey<236:
                                buildTower('r')

                                '''30'''
                            elif 70<mousex<130+greenchoice.get_width() and 250<mousey<306:
                                buildTower('g')

                                '''40'''
                            elif 70<mousex<130+greenchoice.get_width() and 320<mousey<376:
                                buildTower('y')

                                '''Back'''
                            elif 270<mousex<270+backtext.get_width() and 400<mousey<456:
                                pass
                            hslabel = myfont3.render("High Score: "+str(data["BuildingBlox"]["highScore"])+" Residents", 1, (0, 0, 0))
                            chooselevel = False
                            menu = True
                        elif instructionsscreen:
                            '''Left arrow'''
                            if 5<mousex<31 and 190<mousey<290:
                                instrslide -= 1

                                '''Right arrow'''
                            elif 609<mousex<635 and 190<mousey<290:
                                instrslide += 1
                    else:
                        pass  # does nothing for all other input events

                screen.blit(background, (0, 0))
                if menu:
                    screen.blit(title,(140,40))
                    screen.blit(playgame, (230,180))
                    screen.blit(instructions, (230,260))
                    screen.blit(gamemenu, (230,340))
                    screen.blit(hslabel, (20, 440))
                elif chooselevel:
                    screen.blit(difficulty,(180,30))
                    screen.blit(blue,(70,110))
                    screen.blit(bluechoice, (130,110))
                    screen.blit(red,(70,180))
                    screen.blit(redchoice, (130, 180))
                    screen.blit(green,(70,250))
                    screen.blit(greenchoice, (130, 250))
                    screen.blit(yellow,(70,320))
                    screen.blit(yellowchoice, (130, 320))
                    screen.blit(backtext,(270,400))
                elif instructionsscreen:
                    if 0<instrslide<10:
                        slide = pygame.image.load(os.path.join(scriptDir,"images/instructions/instr"+str(instrslide)+".png")).convert_alpha()
                        leftarr = pygame.image.load(os.path.join(scriptDir,"images/instructions/leftarrow.png")).convert_alpha()
                        rightarr = pygame.image.load(os.path.join(scriptDir,"images/instructions/rightarrow.png")).convert_alpha()
                        screen.blit(slide, (0, 0))
                        screen.blit(leftarr, (5, 190))
                        screen.blit(rightarr, (609, 190))
                    else:
                        instrslide = 0
                        instructionsscreen = False
                        menu = True
                screen.blit(musicbutton, (10,10))
                pygame.display.flip()  # Refresh the display





        def buildTower(colour):

            if colour == 'b' :
                tower = classes.BlueTower(0)
            elif colour == 'r':
                tower = classes.RedTower(0)
            elif colour == 'g':
                tower = classes.GreenTower(0)
            elif colour == 'y':
                tower = classes.YellowTower(0)

            '''Fonts and Text'''
            myfont = pygame.font.Font(os.path.join(scriptDir,"fonts/jtwya.ttf"), 19)
            myfont.set_bold(True)
            myfont2 = pygame.font.Font(os.path.join(scriptDir,"fonts/jtwya.ttf"), 28)
            myfont2.set_bold(True)
            resfont = pygame.font.SysFont("monospace", 32, True)

            oklabel = myfont.render("OK ", 1, (0, 0, 0))
            completelabel = myfont.render("Tower Complete!", 1, (0, 0, 0))
            perfectlabel = myfont2.render("Perfect!", 1, (0, 0, 153))
            '''Load images'''
            img = pygame.image.load(os.path.join(scriptDir,tower.getBottomimg())).convert_alpha()  # loads the image for a tower block to img
            wire = pygame.image.load(os.path.join(scriptDir,"images/Tower/wire.png")).convert_alpha()  # loads the image for the swinging wire to wire
            cable = pygame.image.load(os.path.join(scriptDir,"images/Tower/cable.png")).convert_alpha()  # loads the image for cable fir top and bottom blocks

            heart = pygame.image.load(os.path.join(scriptDir,"images/Tower/heart.png")).convert_alpha()
            frame = pygame.image.load(os.path.join(scriptDir,"images/Tower/frame.png")).convert_alpha()
            floorind = pygame.image.load(os.path.join(scriptDir,"images/Tower/floorindicator.png")).convert_alpha()
            resicon = pygame.image.load(os.path.join(scriptDir,"images/Tower/residenticon.png")).convert_alpha()
            comboframe = pygame.image.load(os.path.join(scriptDir,"images/Tower/barframe.png")).convert_alpha()
            combobar = pygame.image.load(os.path.join(scriptDir,"images/Tower/bar.png")).convert_alpha()
            doge = pygame.image.load(os.path.join(scriptDir,"images/Tower/doge.png")).convert_alpha()

            musicbutton = pygame.image.load(os.path.join(scriptDir,"images/Tower/musicbutton.png")).convert_alpha()
            mainmenubutton = pygame.image.load(os.path.join(scriptDir,"images/Tower/mainmenubutton.png")).convert_alpha()

            # loads the image for the skyline background to background
            background = pygame.image.load(os.path.join(scriptDir,"images/Tower/sky.png")).convert()

            global musicplaying
            global residents
            residents = 0

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
            bonusblocks = 0  # list, stores the bonus points for each block in a bonus streak
            secondsleft = 0

            resinc = 0
            comboinc = 0
            scalecombobar = combobar
            framecount2 = 0
            endcombo = False
            highscore = False

            imgheight = img.get_height()
            perflanding = 0

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
                        mousepos = pygame.mouse.get_pos()
                        mousex = mousepos[0]
                        mousey = mousepos[1]
                        '''Music button'''
                        if 10<mousex<81 and 10<mousey<35:
                            if musicplaying:
                                pygame.mixer.music.pause()
                                musicplaying = False
                            else:
                                pygame.mixer.music.unpause()
                                musicplaying = True

                            '''Main Menu Button'''
                        elif 90<mousex<161 and 10<mousey<35:
                            if perfect:
                                perfect = False
                                bonusblocks = 0
                                residents += comboinc
                                endcombo = True
                                framecount2 = 96
                                comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                comboinc = 0
                            blitframe = True
                            populationlabel = myfont.render("Population: "+str(residents), 1, (0, 0, 0))
                            floorlevel = myfont.render("Floors: "+str(len(blockslanded)), 1, (0, 0, 0))
                            #high score
                            if residents > data["BuildingBlox"]["highScore"]:
                                # updating the high score with the new high score.
                                highscore = True
                                highscorelabel = myfont.render("New High Score!", 1, (0, 0, 0))

                            '''OK button'''
                        elif blitframe == True and 310<mousex<310+oklabel.get_width() and 275<mousey<294:
                            updateDatabase()
                            keep_going = False
                        else:
                            haveblock = False  # treats as if down key was pressed
                    else:
                        pass  # does nothing for all other input events

                '''Shifting the background gradually'''

                if imgheight - backgroundinc > 10:
                    backgroundinc += 10.0
                    if shiftdown:
                        yposition += 10.0
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() + 10.0)
                    else:
                        yposition -= 10.0
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() - 10.0)
                elif imgheight - backgroundinc < 10:

                    if shiftdown:
                        yposition += (imgheight - backgroundinc)
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() + imgheight-backgroundinc)
                    else:
                        yposition -= (imgheight - backgroundinc)
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() - (imgheight-backgroundinc))
                    backgroundinc = imgheight
                    shiftdown = True

                '''Tilting effect'''
                if tilt:
                    if abs(tiltdeg)<=0.5:
                        tiltdeg = 0
                        blockslanded[-1].setyPos(blockslanded[-2].getyPos()-imgheight)
                        tilt = False
                    elif tiltdeg>0:
                        tiltdeg -= 0.5
                        blockslanded[-1].setyPos(blockslanded[-1].getyPos() + 0.35)
                    elif tiltdeg<0:
                        tiltdeg += 0.5
                        blockslanded[-1].setyPos(blockslanded[-1].getyPos() + 0.35)
                    #if len(blockslanded) == tower.getMaxLevel()-1:
                    blockslanded[-1].setImg(pygame.transform.rotate(pygame.image.load(os.path.join(scriptDir,tower.getMidimg())).convert_alpha(),tiltdeg))

                '''Perfect landing effect'''
                if perfect:
                    framecount -= 1
                    secondsleft = (framecount/32) + 1
                    scalecombobar = pygame.transform.scale(combobar, (int(framecount*(27.0/32.0)), 5))
                    if framecount == 0 or len(blockslanded) == tower.getMaxLevel():
                        perfect = False
                        bonusblocks = 0
                        residents += comboinc
                        if endcombo == False:
                            endcombo = True
                            framecount2 = 96
                            comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                        comboinc = 0

                '''Display comboinc after combo streak ends'''
                if endcombo:
                    framecount2 -= 1
                    if framecount2 == 0:
                        endcombo = False

                '''Main loop for tower game, continues until game is finished'''
                if len(blockslanded) < tower.getMaxLevel() and lives > 0 and blitframe == False:
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
                            if abs(blockdiff) < 4:
                                perfect = True
                                framecount = 160  # 5 seconds
                                resinc = (len(blockslanded)/20)+5
                                blockx -= blockdiff
                                perflanding = 32
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
                                comboinc += secondsleft*bonusblocks
                                bonusblocks += 1


                            newblock = classes.Block(blockx-swaypos, blocky, resinc, img)
                            blockslanded.append(newblock)

                            imgheight = img.get_height()

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
                                    tiltimg = pygame.transform.rotate(blockslanded[-1].getImg(), tiltdeg)
                                    blockslanded[-1].setImg(tiltimg)
                                    blockslanded[-1].setyPos(blockslanded[-1].getyPos()-(tiltimg.get_height()-imgheight-(abs(blockdiff)*math.sin(abs(tiltdeg)*3.1416/180.0))))
                                    tilt = True

                            if len(blockslanded) == 1:  # after first block
                                img = pygame.image.load(os.path.join(scriptDir,tower.getMidimg())).convert_alpha()  # loads the image for a tower block to img
                                wire = pygame.image.load(os.path.join(scriptDir,"images/Tower/hookwire.png")).convert_alpha()  # loads the image for the swinging wire to wire
                                rotImg = pygame.transform.rotate(img, degrees)
                                blitblock = False

                            elif len(blockslanded) == (tower.getMaxLevel() - 1):
                                img = pygame.image.load(os.path.join(scriptDir,tower.getTopimg())).convert_alpha()  # loads the image for a tower block to img
                                wire = pygame.image.load(os.path.join(scriptDir,"images/Tower/wire.png")).convert_alpha()  # loads the image for the swinging wire to wire
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
                                        imgheight = img.get_height()

                                        if perfect:
                                            perfect = False
                                            bonusblocks = 0
                                            residents += comboinc
                                            endcombo = True
                                            framecount2 = 96
                                            comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                            comboinc = 0

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
                                    if perfect:
                                        perfect = False
                                        bonusblocks = 0
                                        residents += comboinc
                                        endcombo = True
                                        framecount2 = 96
                                        comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                        comboinc = 0


                else:
                    blitframe = True
                    populationlabel = myfont.render("Population: "+str(residents), 1, (0, 0, 0))
                    floorlevel = myfont.render("Floors: "+str(len(blockslanded)), 1, (0, 0, 0))
                    #high score
                    if residents> data["BuildingBlox"]["highScore"]:
                        # updating the high score with the new high score.
                        highscore = True
                        highscorelabel = myfont.render("New High Score!", 1, (0, 0, 0))

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
                floorx = 65-floorlabel.get_width()/2
                screen.blit(floorlabel, (floorx, 416))

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
                screen.blit(resicon, (480, 30))
                totalres = "0"*(5-len(str(residents)))+str(residents)
                totresdis = myfont2.render(totalres, 1, (255, 255, 255))
                screen.blit(totresdis, (505, 25))

                '''Bonus streak bar and glow'''
                if perfect:
                    bonuseqn = myfont2.render(str(secondsleft) + " x " + str(bonusblocks), 1, (255, 255, 0))
                    screen.blit(bonuseqn, (290, 410))
                    screen.blit(comboframe, (380, 425))
                    screen.blit(scalecombobar, (385, 432))
                    screen.blit(doge, (580, 420))

                '''Perfect Landing'''
                if perflanding != 0:
                    perflanding -= 1
                    screen.blit(perfectlabel, (150, 250))

                '''End combo display'''
                if endcombo:
                    screen.blit(comboincdisplay, (70, 80))

                '''Music and Main Menu buttons'''
                screen.blit(musicbutton, (10,10))
                screen.blit(mainmenubutton, (90,10))

                '''Ending screen'''
                if blitframe:
                    screen.blit(frame, (170, 100))
                    if len(blockslanded) == tower.getMaxLevel():
                        screen.blit(completelabel, (240, 110))
                    screen.blit(populationlabel, (220, 150))
                    screen.blit(floorlevel, (220, 180))
                    #high score
                    if highscore:
                        screen.blit(highscorelabel, (220, 240))
                    screen.blit(oklabel, (310, 275))

                pygame.display.flip()  # Refresh the display

            return residents
        mainMenu()
