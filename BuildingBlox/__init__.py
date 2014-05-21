'''
Programmer: Benjamin Li
Program Name: BuildingBlox.py (BuildingBlox/__init__.py)
Project Name: City Manager
Purpose: Main file for the Building Blox game. Includes tower building and menu interfaces
Date: May 20, 2014
'''

# imports pygame modules
import pygame
from pygame.locals import *

# import Building Blox classes
import classes

# import python libraries
import math
import os

# import database read/write tools
import yaml

# saves the path for the file for future use
scriptDir = os.path.dirname(__file__)

# Class for tower building game. Will be called in game suite main menu
class BuildingBlox():

    """
    Pre: User is on game suite main menu and chooses to play Building Blox game.
    Post: Building Blox game finishes and user returns to the game suite menu
    Purpose: Runs the Building Blox mini game by launching the game menu
    """
    def run(self):

        ''' Database '''
        with open(os.path.join(scriptDir, "../shared_data.yaml"), 'r') as shared_data:  # Opening the database as read-only
            # Storing all the data inside the database to the data variable.
            data = yaml.load(shared_data)

        '''Pygame Display'''
        # initializes the pygame module
        pygame.init()
        # initialized the font module from pygame
        pygame.font.init()
        # Creates and initializes clock to control frame rate
        clock = pygame.time.Clock()
        #Set-up the main display window and the background
        size = (640, 480)
        #Screen: Surface object, serves as the base of the GUI to display other surfaces on
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Building Blox")  # Sets title bar caption

        '''Music'''
        pygame.mixer.music.load(os.path.join(scriptDir, "sound/music.wav"))
        pygame.mixer.music.play(-1)  # Plays music (repeats indefinitely)
        musicplaying = True  # Boolean, used to keep track of whether music is playing (True) or paused (False)

        # Initializes the number of residents (score) of the tower
        residents = 0

        """
        Pre: The data must be defined and must contain the previous the shared_data.yaml contents.
        Post: Database is updated with the information from the Building Blox game
        Purpose: To save the data from the Building Blox game to a shared database.
        """
        def updateDatabase():
            global residents

            # opening the shared_data.yaml file.
            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'w') as shared_data:

                # Checks if the score of the current game surpasses the high score recorded on the database
                if residents > data["BuildingBlox"]["highScore"]:
                    # updates the high score
                    data["BuildingBlox"]["highScore"] = residents

                # Increasesthe raw population of the city
                data["shared_data"]["raw_population"] = data["shared_data"]["raw_population"] + residents

                # Updates the total population of the city
                data["shared_data"]["population"] = round(data["shared_data"]["raw_population"] * data["shared_data"]["multiplier"],0)

                """
                A set of if statements to determine the city size.
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

        """
        Pre: BuildingBlox object is initialized in the game suite main menu
        Post: Exits the Building Blox game and returns to the gain suite main menu
        Purpose: Main menu of the Building Blox game. Calls the tower building interface. Includes instructions
                 for the game.
        """
        def mainMenu():

            '''Font'''
            myfont = pygame.font.Font(os.path.join(scriptDir, "fonts/hollow.ttf"), 96)
            myfont.set_bold(False)
            myfont2 = pygame.font.Font(os.path.join(scriptDir, "fonts/hollow.ttf"), 56)
            myfont2.set_bold(False)
            myfont3 = pygame.font.Font(os.path.join(scriptDir, "fonts/hollow.ttf"), 28)
            myfont3.set_bold(False)

            '''Text Labels'''
            title = myfont.render("Building Blox", 1, (0, 0, 0))
            playgame = myfont2.render("Play Game!", 1, (0, 0, 0))
            instructions = myfont2.render("Instructions", 1, (0, 0, 0))
            gamemenu = myfont2.render("Game Suite", 1, (0, 0, 0))
            # High Score label also prints the high score value of the game
            hslabel = myfont3.render("High Score: "+str(data["BuildingBlox"]["highScore"])+" Residents", 1, (0, 0, 0))
            difficulty = myfont2.render("Choose Difficulty:", 1, (0, 0, 0))
            bluechoice = myfont2.render("Apartment (10 Floors)", 1, (0, 0, 0))
            redchoice = myfont2.render("Condo (20 Floors)", 1, (0, 0, 0))
            greenchoice = myfont2.render("Complex (30 Floors)", 1, (0, 0, 0))
            yellowchoice = myfont2.render("Skyscraper (40 Floors)", 1, (0, 0, 0))
            backtext = myfont2.render("Back", 1, (0, 0, 0))

            # Background image for the menu
            background = pygame.image.load(os.path.join(scriptDir,"images/Menu/mainmenubk.png")).convert_alpha()
            # Music toggle image
            musicbutton = pygame.image.load(os.path.join(scriptDir,"images/Tower/musicbutton.png")).convert_alpha()
            # Four images each corresponding to one of the tower levels
            blue = pygame.image.load(os.path.join(scriptDir,"images/Menu/blueComp.png")).convert_alpha()
            red = pygame.image.load(os.path.join(scriptDir,"images/Menu/redComp.png")).convert_alpha()
            green = pygame.image.load(os.path.join(scriptDir,"images/Menu/greenComp.png")).convert_alpha()
            yellow = pygame.image.load(os.path.join(scriptDir,"images/Menu/yellowComp.png")).convert_alpha()

            # Recognized that these variables are global in the run() function
            global residents
            global musicplaying
            musicplaying = True

            keep_going = True  # Boolean, serves as condition for game loop to repeat

            #Initialize variables used to determine where the user is at on the menu
            menu = True  # Boolean, True if user is on the Building Blox menu
            chooselevel = False  # Boolean, True if user is on the "choose difficulty" screen
            instructionsscreen = False  # Boolean, True if user is viewing the instructions for the game

            instrslide = 0  # integer, stores the slide of the instructions that the user is on

            # Pygame display loop for the Building Blox main menu
            while keep_going:

                #Handle  events in the frame
                for ev in pygame.event.get():
                    if ev.type == QUIT:  # happens when the window is closed
                        keep_going = False

                    elif ev.type == MOUSEBUTTONDOWN:  # if the mouse was clicked
                        mousepos = pygame.mouse.get_pos()  # gets the position of the mouse
                        mousex = mousepos[0]
                        mousey = mousepos[1]

                        '''Music toggle button'''

                        if 10<mousex<81 and 10<mousey<35:

                            if musicplaying:  # pauses music if music was playing
                                pygame.mixer.music.pause()
                                musicplaying = False
                            else:  # resumes music if music was paused
                                pygame.mixer.music.unpause()
                                musicplaying = True

                            '''Main Menu Buttons'''
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
                                keep_going=False  # This causes the display to stop refreshing
                                pygame.mixer.music.stop()  # Stops the Building Blox background music

                            '''Choose Difficulty Menu'''
                        elif chooselevel:
                            '''10 Floors'''
                            if 70<mousex<130+bluechoice.get_width() and 110<mousey<166:
                                buildTower('b')  # Plays with blue tower

                                '''20'''
                            elif 70<mousex<130+redchoice.get_width() and 180<mousey<236:
                                buildTower('r')  # Plays with red tower

                                '''30'''
                            elif 70<mousex<130+greenchoice.get_width() and 250<mousey<306:
                                buildTower('g')  # Plays with green tower

                                '''40'''
                            elif 70<mousex<130+greenchoice.get_width() and 320<mousey<376:
                                buildTower('y')  # Plays with yellow tower

                                '''Back button does not need unique commands'''
                            # Renders the high score label in case the high score was changed after the previous game
                            hslabel = myfont3.render("High Score: "+str(data["BuildingBlox"]["highScore"])+" Residents", 1, (0, 0, 0))
                            chooselevel = False
                            menu = True

                            '''Instructions'''
                        elif instructionsscreen:
                            '''Left arrow'''
                            if 5<mousex<31 and 190<mousey<290:
                                instrslide -= 1

                                '''Right arrow'''
                            elif 609<mousex<635 and 190<mousey<290:
                                instrslide += 1
                    else:
                        pass  # does nothing for all other input events

                screen.blit(background, (0, 0))  # Background image is displayed since it is used in all parts of the
                                                 # main menu
                # Displays surfaces corresponding to the main menu
                if menu:
                    screen.blit(title,(140,40))
                    screen.blit(playgame, (230,180))
                    screen.blit(instructions, (230,260))
                    screen.blit(gamemenu, (230,340))
                    screen.blit(hslabel, (20, 440))

                # Displays surfaces corresponding with the choose difficulty menu
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

                # Displays surfaces corresponding with the instructions interface
                elif instructionsscreen:
                    if 0<instrslide<10:  # Returns to main menu when instrslide is beyond the number of images in the
                                         # instructions interface

                        # Loads required images
                        slide = pygame.image.load(os.path.join(scriptDir,"images/instructions/instr"+str(instrslide)+".png")).convert_alpha()
                        leftarr = pygame.image.load(os.path.join(scriptDir,"images/instructions/leftarrow.png")).convert_alpha()
                        rightarr = pygame.image.load(os.path.join(scriptDir,"images/instructions/rightarrow.png")).convert_alpha()
                        screen.blit(slide, (0, 0))
                        screen.blit(leftarr, (5, 190))
                        screen.blit(rightarr, (609, 190))
                    else:  # When the user is beyond the maximum or minimum slide, returns to the Building Blox menu
                        # Resets variables to when user was on the main menu
                        instrslide = 0
                        instructionsscreen = False
                        menu = True

                # Displays the music toggle button
                screen.blit(musicbutton, (10,10))

                pygame.display.flip()  # Refresh the display

        """
        Pre: User is on Choose Difficulty menu of the Building Blox menu and selects a difficulty
        Post: User finishes the game and returns to the Building Blox main menu. Database is updated
        Purpose: This the main game method for building blox. Allows the user to play the game and build a tower.
        """
        def buildTower(colour):

            # Creates different colored tower based on difficulty level chosen
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

            # Recognized that these variables are global in the run() function
            global musicplaying
            global residents
            residents = 0

            yposition = -2880.0  # float, vertical position to display the background. Initialized to show base of background
            wirebasex = 210.0     # constant float, initial horizontal position for wire. Future positions are based on this
            wirebasey = -150.0    # constant float, initial vertical position for wire. Future positions are based on this
            wirex = 0.0  # float, horizontal distance in addition to wirebasex
            wirey = 0.0  # float, vertical distance in addition to wirebasey
            wireyinc = 2.0  # represents the amount added to wirey every frame. Changes signs every time 0 degrees is passed
            cablex = 0.0  # float, horizontal position of the cable (for first and last blocks)
            cabley = 0.0  # float, vertical position of the cable (for the first and last blocks)

            screen.blit(background, (0, yposition))  # Places the background at the starting position
            degrees = -20  # integer, degree at which surface objects are rotated; Counterclockwise is positive

            # Initial rotation of tower block and wire
            rotImg = pygame.transform.rotate(img,0)
            rotImg2 = pygame.transform.rotate(wire,degrees)

            # blockx: float, horizontal position of block surface. Calculated every frame based on position of the wire.
            blockx=float(wirex+wirebasex - (rotImg.get_width()/2))
            # blockx: float, vertical position of tower block surface. Calculated every frame based on position of the wire.
            blocky=float(wirey + wirebasey + rotImg2.get_height() - float((rotImg.get_height()/2)))
            blockoffset = 35.0  # float, value used to account for the difference in height of block images

            # Displays the wire and the block onto the background
            screen.blit(rotImg2,(float(wirex + wirebasex), float(wirey + wirebasey)))
            screen.blit(rotImg, (blockx, blocky))

            keep_going = True  # boolean, controls whether the game loop continues

            # list, stores Block objects for the landed blocks
            blockslanded = []

            lives = 3  # integer, stores the number of lives left. When this hits 0, game ends
            imperfect = 0  # integer, number of imperfectly landed blocks, used to calculate sway effect
            sway = 0.0  # float, horizontal number of pixels the tower needs to wobble
            swaypos = 0.0  # float, horizontal number of pixels swayed in the current frame
            swayinc = sway/16.0  # float, number of pixels moved per frame
            waitframe = 10  # integer, counter variable used to make the tower stay at either end of the wobble for 10 frames

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
            backgroundinc = img.get_height()  # float, amount that the background needs to shift after block lands/is knocked out

            passedlastblock = False  # Boolean, True if the block lands correctly and the height of the tower increases

            blitframe = False  # Boolean variable, prevents the block from being displayed immediately after img change
            tilt = False  # Boolean variable, used to initiate the tilt animation after a block successfully lands
            eligible = True  # Boolean variable, used to ensure that position of block (hit or miss) is only evaluated once
            tumble = False  # Boolean variable to initiate tumbling of previous block due to imperfect landing
            shiftdown = True  # Boolean variable, determines whether the background should shift up or down
            perfect = False  # Boolean variable, set to True when the block lands perfectly
            framecount = 0  # integer, counts the number of frames for long lasting events
            bonusblocks = 0  # list, stores the bonus points for each block in a bonus streak
            secondsleft = 0  # integer, stores the integer value of the time left in the bonus period

            resinc = 0  # integer, amount the number of residents (score) increases by after a block lands
            comboinc = 0  # integer, tally of the number of residents to add to total residents after bonus period ends
            scalecombobar = combobar  # Surface, a bar with lenght modified depending on time left in the bonus period
            framecount2 = 0  # integer, counter used to display comboinc for 3 seconds (96 frames)
            endcombo = False  # Boolean, signals when the bonus period ends in order to start displaying comboinc
            highscore = False  # Boolean, True if the score in the current game exceeds the record on the database

            imgheight = img.get_height()  # integer, stores the height of the block image, used because the image changes
            perflanding = 0  # integer, used to count the frames in order to display 'Perfect!' after a combo starts

            # Game loop
            while keep_going:

                # Floors constructed/Max floors label
                floorlabel = myfont.render(str(len(blockslanded))+"/"+str(tower.getMaxLevel()), 1, (255, 255, 255))

                clock.tick(32) # sets frame rate at 32 fps

                #Handle  events in the frame
                for ev in pygame.event.get():
                    if ev.type == QUIT:
                        keep_going = False  # exits Building Blox when window is closed

                    elif ev.type == KEYDOWN:
                        if ev.key == K_DOWN:  # drops block
                            haveblock = False

                    elif ev.type == MOUSEBUTTONDOWN:  # if the mouse was clicked
                        mousepos = pygame.mouse.get_pos()
                        mousex = mousepos[0]
                        mousey = mousepos[1]

                        '''Music button'''
                        if 10<mousex<81 and 10<mousey<35:
                            if musicplaying:  # Pauses music if music was playing
                                pygame.mixer.music.pause()
                                musicplaying = False
                            else:  # Resumes music if music was paused
                                pygame.mixer.music.unpause()
                                musicplaying = True

                            '''Main Menu Button'''
                        elif 90<mousex<161 and 10<mousey<35:
                            if perfect:  # Stops combo if user goes back to menu
                                perfect = False
                                bonusblocks = 0
                                residents += comboinc
                                endcombo = True
                                framecount2 = 96
                                comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                comboinc = 0
                            # Displays summary for the game
                            blitframe = True
                            populationlabel = myfont.render("Population: "+str(residents), 1, (0, 0, 0))
                            floorlevel = myfont.render("Floors: "+str(len(blockslanded)), 1, (0, 0, 0))

                            # Checks if high score was achieved
                            if residents > data["BuildingBlox"]["highScore"]:
                                # updating the high score with the new high score.
                                highscore = True
                                highscorelabel = myfont.render("New High Score!", 1, (0, 0, 0))

                            '''OK button'''
                        elif blitframe == True and 310<mousex<310+oklabel.get_width() and 275<mousey<294:
                            updateDatabase()  # Updates the database
                            keep_going = False
                        else:
                            haveblock = False  # treats as if down key was pressed
                    else:
                        pass  # does nothing for all other input events

                '''Shifting the background gradually'''
                if imgheight - backgroundinc > 10:  # shifts 10 pixels until there are few than 10 pixels left
                    backgroundinc += 10.0
                    if shiftdown:
                        yposition += 10.0
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() + 10.0)
                    else:
                        yposition -= 10.0  # shifts opposite direction when block is knocked off
                        for blk in blockslanded:
                            blk.setyPos(blk.getyPos() - 10.0)
                elif imgheight - backgroundinc < 10:  # shifts remaining pixels

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

                            # Increases sway effect as the tower gets taller
                            if len(blockslanded) % 5 == 0 and imperfect > 0:
                                sway += 5.0

                            '''Operations for bonus streak'''
                            if perfect:
                                comboinc += secondsleft*bonusblocks
                                bonusblocks += 1

                            # Stores the block that was just landed into a list
                            newblock = classes.Block(blockx-swaypos, blocky, resinc, img)
                            blockslanded.append(newblock)

                            imgheight = img.get_height()

                            haveblock = True  # changes boolean value so that a new block may be generated back on the wire
                            passedlastblock = False
                            fallxisset = False  # changes boolean value so that fallx may be reset
                            falltime = 0  # sets amount of frames after falling back to 0
                            eligible = True  # blocks are eligible to be checked for landing position hit/miss

                            '''Landing tilt animation'''
                            if tower.getMaxLevel() > len(blockslanded) > 1:
                                backgroundinc = 0
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

                            elif len(blockslanded) == (tower.getMaxLevel() - 1):  # Before last block
                                img = pygame.image.load(os.path.join(scriptDir,tower.getTopimg())).convert_alpha()  # loads the image for a tower block to img
                                wire = pygame.image.load(os.path.join(scriptDir,"images/Tower/wire.png")).convert_alpha()  # loads the image for the swinging wire to wire
                                rotImg = pygame.transform.rotate(img, 0)
                                if tower.getMaxLevel() == 40:
                                    blockoffset = 95.0
                                blitblock = False
                        else:  # If block misses/knocks off previous block, or is still falling
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

                            # Spins the block when tumbling
                            rotImg = pygame.transform.rotate(img, falldegrees*tumbleinc)
                            blocky += fally

                            if eligible == True:  # Prevents block to be evaluated (hit/miss) more than once
                                blockdiff = 100 # Assigns an arbitrary number so that the first block cannot miss
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

                                        # Ends combo
                                        if perfect:
                                            perfect = False
                                            bonusblocks = 0
                                            residents += comboinc
                                            endcombo = True
                                            framecount2 = 96
                                            comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                            comboinc = 0

                                        # Starts a new parabolic path for motion
                                        fallxisset = False  # changes boolean value so that fallx may be reset
                                        falltime = 0  # sets amount of frames after falling back to 0
                                        tempimg = blockslanded[-1].getImg()
                                    eligible = False

                            else:
                                '''Tumbling animation when current block knocks out previous block'''
                                if tumble:
                                    # Position of previous block is calculated based on position of current block while tumbling
                                    if tower.getMaxLevel()-1 > len(blockslanded) > 1:
                                        blockslanded[-1].setImg(pygame.transform.rotate(tempimg, falldegrees))
                                        blockslanded[-1].setxPos(blockslanded[-1].getxPos()-fallx)
                                        blockslanded[-1].setyPos(blocky+img.get_height())

                                if blocky > 480:  # When the block drops beyond the screen
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
                                    #Ends combo
                                    if perfect:
                                        perfect = False
                                        bonusblocks = 0
                                        residents += comboinc
                                        endcombo = True
                                        framecount2 = 96
                                        comboincdisplay = resfont.render("+"+str(comboinc), 1, (0, 255, 0))
                                        comboinc = 0
                else:  # When the game ends
                    # Displays endgame summary
                    blitframe = True
                    populationlabel = myfont.render("Population: "+str(residents), 1, (0, 0, 0))
                    floorlevel = myfont.render("Floors: "+str(len(blockslanded)), 1, (0, 0, 0))
                    # Check if score for this game is higher than the one recorded in the database
                    if residents> data["BuildingBlox"]["highScore"]:
                        # updating the high score with the new high score.
                        highscore = True
                        highscorelabel = myfont.render("New High Score!", 1, (0, 0, 0))

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
        mainMenu() # runs the main menu to start the Building Blox game
