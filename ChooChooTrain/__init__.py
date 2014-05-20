
import pygame
import random
import math
from pygame.locals import *
from random import randint
import os
import yaml
import webbrowser


scriptDir = os.path.dirname(__file__)

pygame.init()
pygame.mixer.init()

size = (840, 640)
size2=(900,600)
screen = pygame.display.set_mode(size)  # initialize screen, the window where all the graphics are pasted on

trackgrid=[]    # trackgrid is a list that contains all 64 instances of the train tracks
click=[]        # click is a list that contains all the grid numbers of the grids that the user clicked on

grid = random.sample(range(64), 64)
gridtype=[]
for i in range (64):
    gridtype.append(randint(0,1))

imgs=[]         #imgs is a list that contains all the grid images

# trainx and trainy are the initial positions of the train
trainx=520
trainy=240

specialpic=[]   #specialpic is a list that contains all the icons of the special items
pic1 = pygame.image.load(os.path.join(scriptDir,"img/gas.jpeg"))
pic1 = pygame.transform.scale(pic1,(30,30))
specialpic.append(pic1)
pic2=pygame.image.load(os.path.join(scriptDir,"img/bump.png"))
pic2 = pygame.transform.scale(pic2,(30,30))
specialpic.append(pic2)


trainimg=[] # trainimg is a list that contains all the icons of the train
train1 = pygame.image.load(os.path.join(scriptDir,"img/train.png"))
train1 = pygame.transform.scale(train1,(60,60))
trainimg.append(train1)
train2=pygame.image.load(os.path.join(scriptDir,"img/train2.png"))
train2 = pygame.transform.scale(train2,(60,60))
trainimg.append(train2)
train3=pygame.image.load(os.path.join(scriptDir,"img/train3.png"))
train3 = pygame.transform.scale(train3,(60,60))
trainimg.append(train3)

startpoint = [28]       #startpoint is a list that contains all the connected grids
timepergrid = 1.0     # timepergrid controls the speed of the train

set1=[1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,0,0,0,1,0,1, 1,1,1,1,1,0,1,1 ,1,1,1,1,1,1,1,1, 1,1,1,0,1,1,1,1, 1,1,1,1,1,1,1,1]
#initialize the backgroud music


diff=0   #diff is used to reset the timer
lastgrid=28


counter2=0


score=0
class ChooChooTrain():

    def run(self):

        # Opening the database as read-only
        with open(os.path.join(scriptDir, "../shared_data.yaml"), 'r') as shared_data:
            # Storing all the data inside the database to the data variable.
            data = yaml.load(shared_data)

        pygame.init()  # initializes the pygame module

        pygame.mixer.music.load(os.path.join(scriptDir, "sound/train_music.wav"))
        pygame.mixer.music.play(-1)

        size = (840, 640)
        screen= pygame.display.set_mode(size)
        def updateDatabase():
            global residents
            # opening the shared_data.yaml file.
            with open(os.path.join(scriptDir, "../shared_data.yaml"), 'w') as shared_data:
                mark=len(startpoint)
                if mark > data["ChooChooTrain"]["highScore"]:
                    # updating the high score with the new high score.
                    data["ChooChooTrain"]["highScore"] = score
                #increasing the raw population of the city
                if mark<50:
                    data["shared_data"]["multiplier"]=1.1
                elif mark<100:
                    data["shared_data"]["multiplier"]=1.2
                elif mark<150:
                    data["shared_data"]["multiplier"]=1.3
                elif mark<200:
                    data["shared_data"]["multiplier"]=1.4
                else:
                    data["shared_data"]["multiplier"]=1.5

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
        def timereset(currenttime): #this function resets the timer everytime the game is replayed
            global  diff
            diff=currenttime

        def connectcheck(track,start):  #this function checks whether two grids connect
            bCon=False

            if track.getNumber()-8 == start or track.getNumber()+8 == start: # the two grids are on top or below each other
                if track.getSc()==0 and trackgrid[start].getSc()==0:    #both are straight
                    if track.getOrient()%2==0 and trackgrid[start].getOrient()%2==0: # both are sideways
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)
                elif trackgrid[start].getSc()==0 and track.getSc()==1 and track.getNumber()+8 == start: # straight on bottom (start) and curve on top (track)
                    if trackgrid[start].getOrient()%2==0 and track.getCont()==1: # straight and curve (orientation1)
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)

                elif trackgrid[start].getSc()==0 and track.getSc()==1 and track.getNumber()-8 == start:#
                    if trackgrid[start].getOrient()%2==0 and track.getOrient()>1:
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)

                elif trackgrid[start].getSc()==1 and track.getSc()==0 and track.getNumber()+8 == start:
                    if trackgrid[start].getOrient()>1 and track.getOrient()%2==0:
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)
                elif trackgrid[start].getSc()==1 and track.getSc()==0 and track.getNumber()-8 == start:
                    if trackgrid[start].getOrient()<2 and track.getOrient()%2==0:
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)
                elif trackgrid[start].getSc()==1 and track.getSc()==1 and track.getNumber()+8 == start: #curve on curve (track on top)

                    if trackgrid[start].getOrient()>1 and track.getOrient()<2:
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)
                elif trackgrid[start].getSc()==1 and track.getSc()==1 and track.getNumber()-8 == start:
                    if trackgrid[start].getOrient()<2 and track.getOrient()>1:
                        track.setWp(1)
                        bCon=True
                        trackgrid[start].setlock(True)
            elif track.getNumber()+1 == start or track.getNumber()-1 == start:
                if track.getNumber()/8 == start/8:
                    if track.getSc()==0 and trackgrid[start].getSc()==0:
                        if track.getOrient()%2==1 and trackgrid[start].getOrient()%2==1:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==0 and track.getSc()==1 and track.getNumber()+1 == start: # straight and curve on top
                        if trackgrid[start].getOrient()%2==1 and track.getCons()==1:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==0 and track.getSc()==1 and track.getNumber()-1 == start:
                        if trackgrid[start].getOrient()%2==1 and track.getCons()==0:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==1 and track.getSc()==0 and track.getNumber()+1 == start:
                        if trackgrid[start].getCons()==0 and track.getOrient()%2==1:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==1 and track.getSc()==0 and track.getNumber()-1 == start:
                        if trackgrid[start].getCons()==1 and track.getOrient()%2==1:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==1 and track.getSc()==1 and track.getNumber()+1 == start:
                        if trackgrid[start].getCons()==0 and track.getCons()==1:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
                    elif trackgrid[start].getSc()==1 and track.getSc()==1 and track.getNumber()-1 == start:
                        if trackgrid[start].getCons()==1 and track.getCons()==0:
                            track.setWp(1)
                            bCon=True
                            trackgrid[start].setlock(True)
            if startpoint==[]:
                startpoint.append(28)
            if bCon == True:
                startpoint.append(track.getNumber())    # add the newly connected grid to the startpoint

            return bCon

        def changecolor(track,start):   # this changes the colour of the connected grids
            try:
                if track.getNumber()!= start:   # if the clicked grid is not the last clicked grid
                    btf = connectcheck(track,start) #then check if the clicked grid is connected
                    if btf==False:      # if it is not then change to white
                        track.setWp(0)
                else:
                    startpoint.pop(-1)  # if it is the last connected grid
                    btf = connectcheck(track,startpoint[-1])    # then check if it is connected to the last clicked grid
                    if btf==False:  # if it is not, then change to white
                        track.setWp(0)
                if btf ==True:  # if the connected grid is connected
                    for i in range(64):
                        btf=findUnconnectedEnd(trackgrid[startpoint[-1]])   #then check if it can auto-connect more grids
                        if btf ==False:
                            break

            except:
                pass

        def findUnconnectedEnd(track):  #this function is used to auto-connect other grids to the last clicked grid
            try:
                if track.getSc() == 0:
                    if track.getOrient()%2 ==0: #straignt and topbottom

                            if trackgrid[track.getNumber()-8].getWp()==1 and trackgrid[track.getNumber()+8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()+8],track.getNumber())


                            elif trackgrid[track.getNumber()+8].getWp()==1 and trackgrid[track.getNumber()-8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()-8],track.getNumber())


                    elif track.getOrient()%2==1:
                        #if track.getNumber()-1>-1 and (track.getNumber()-1)/8==track.getNumber()/8:
                            if trackgrid[track.getNumber()-1].getWp()==1 and trackgrid[track.getNumber()+1].getWp()==0:
                                if (track.getNumber()-1)/8==track.getNumber()/8:
                                    connectcheck(trackgrid[track.getNumber()+1],track.getNumber())

                        #elif track.getNumber()+1<64 and (track.getNumber()+1)/8==track.getNumber()/8:
                            elif trackgrid[track.getNumber()+1].getWp()==1 and trackgrid[track.getNumber()-1].getWp()==0:
                                if (track.getNumber()+1)/8==track.getNumber()/8:
                                    connectcheck(trackgrid[track.getNumber()-1],track.getNumber())


                elif track.getSc()==1:
                    if track.getCons()==0:
                        if trackgrid[track.getNumber()-1].getWp()==1:
                            if track.getCont()==0 and trackgrid[track.getNumber()-8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()-8],track.getNumber())

                            elif track.getCont()==1 and trackgrid[track.getNumber()+8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()+8],track.getNumber())

                        else:
                            connectcheck(trackgrid[track.getNumber()-1],track.getNumber())

                    elif track.getCons()==1:
                        if trackgrid[track.getNumber()+1].getWp()==1 :
                            if track.getCont()==0 and trackgrid[track.getNumber()-8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()-8],track.getNumber())

                            elif track.getCont()==1 and trackgrid[track.getNumber()+8].getWp()==0:
                                connectcheck(trackgrid[track.getNumber()+8],track.getNumber())

                        else:
                            connectcheck(trackgrid[track.getNumber()+1],track.getNumber())

            except IndexError:
                pass


        def setPos(num,counter):    # sets the path of the train
            global timepergrid
            global lastgrid
            global counter2
            if num==lastgrid:
                counter2+=1
            elif num!=lastgrid:
                counter2=0
                lastgrid=num
            currentgrid=trackgrid[num]
            index=0
            rx=trainx
            ry=trainy
            try:
                    for i in range (len(startpoint)):
                        if startpoint[i]==num:
                            index = i
                    if startpoint[index+1]-num ==1 and currentgrid.getSc()==0: #next grid on the right side
                        rx=trainx+(80/(30*timepergrid))
                        ry=trainy
                        train.setimg(3)
                    elif startpoint[index+1]-num ==-1 and currentgrid.getSc()==0: #next grid on the left side
                        rx=trainx-(80/(30*timepergrid))
                        ry=trainy
                        train.setimg(1)
                    elif startpoint[index+1]-num==8 and currentgrid.getSc()==0: #next grid right below
                        rx=trainx
                        ry=trainy+(80/(30*timepergrid))
                        train.setimg(2)
                    elif startpoint[index+1]-num == -8 and currentgrid.getSc()==0: #next grid right above
                        rx=trainx
                        ry=trainy-(80/(30*timepergrid))

                        train.setimg(2)
                    elif startpoint[index+1]-num ==1 and currentgrid.getSc()==1 and currentgrid.getOrient()==0: #next grid on the right side

                        a = currentgrid.getx()+80
                        b=currentgrid.gety()+80
                        rx=currentgrid.getx()+40+40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)
                        try:
                            ry= b-math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==1 and currentgrid.getSc()==1 and currentgrid.getOrient()==3: #next grid on the right side

                        a = currentgrid.getx()+80
                        b=currentgrid.gety()

                        try:
                            ry= b+math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==-1 and currentgrid.getSc()==1 and currentgrid.getOrient()==1:#next grid on the left side

                        a = currentgrid.getx()
                        b=currentgrid.gety()+80
                        rx=currentgrid.getx()+40-40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b-math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==-1 and currentgrid.getSc()==1 and currentgrid.getOrient()==2: #next grid on the left side

                        a = currentgrid.getx()
                        b=currentgrid.gety()
                        rx=currentgrid.getx()+40-40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b+math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==8 and currentgrid.getSc()==1 and currentgrid.getOrient()==0: #next grid below

                        a = currentgrid.getx()+80
                        b=currentgrid.gety()+80
                        rx=currentgrid.getx()+80-40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b-math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==8 and currentgrid.getSc()==1 and currentgrid.getOrient()==1: #next grid below

                        a = currentgrid.getx()
                        b=currentgrid.gety()+80
                        rx=currentgrid.getx()+40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b-math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==-8 and currentgrid.getSc()==1 and currentgrid.getOrient()==2:#next grid top

                        a = currentgrid.getx()
                        b=currentgrid.gety()
                        rx=currentgrid.getx()+40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b+math.sqrt(1600-(rx-a)**2)
                        except ValueError:
                            ry=b
                        #ry-=3
                        train.setimg(2)

                    elif startpoint[index+1]-num ==-8 and currentgrid.getSc()==1 and currentgrid.getOrient()==3: #next grid top

                        a = currentgrid.getx()+80
                        b=currentgrid.gety()
                        rx=currentgrid.getx()+80-40*math.sin((90/(90*timepergrid)*counter2)*math.pi/180)

                        try:
                            ry= b+math.sqrt(1600-math.pow(rx-a,2))
                        except ValueError:
                            ry=b

                        train.setimg(2)

            except IndexError:
                    pass
            return (rx,ry,)

        def endScreen(time):
            global score
            clock = pygame.time.Clock()
            keep_going = True


            while keep_going:

                clock.tick(30)
                for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                        if ev.type == QUIT: #<-- this special event type happens when the window is closed
                            pygame.mixer.music.stop()
                            keep_going = False

                        elif ev.type == pygame.MOUSEBUTTONDOWN:
                            mousepos = pygame.mouse.get_pos()
                            x = mousepos[0]
                            y = mousepos[1]
                            if x>=200 and x<=340 and y>=500 and y<=555:
                                    keep_going=False
                                    reset()
                                    timereset(pygame.time.get_ticks())
                                    main()
                            elif x>=515 and x<=655 and y>500 and y<=555:
                                    keep_going=False
                                    startMenu()


                if keep_going==True:
                    min = time/60000
                    sec = (time-min*60000)/1000
                    stemp=""
                    if len(str(min))==1 and len(str(sec))==1:
                        stemp = "0"+str(min)+":0"+str(sec)
                    elif len(str(min))==1 and len(str(sec))==2:
                        stemp = "0"+str(min)+":"+str(sec)
                    elif len(str(min))>1 and len(str(sec))==1:
                        stemp = str(min)+":0"+str(sec)
                    score = len(startpoint)


                    output2Font = pygame.font.SysFont("PLAYED FOR   "+str(stemp), 50)
                    output2 = output2Font.render("PLAYED FOR   "+str(stemp), 2, (255,255,255))
                    output3Font = pygame.font.SysFont("* GAME OVER *", 100)
                    output3 = output3Font.render("* GAME OVER *", 3, (255,255,255))
                    output4Font = pygame.font.SysFont("SCORE: "+str(score), 50)
                    output4 = output4Font.render("SCORE: "+str(score), 2, (255,255,255))
                    output5Font = pygame.font.SysFont("Replay", 40)
                    output5= output5Font.render("Replay", 2, (0,0,0))
                    output6Font = pygame.font.SysFont("Back", 40)
                    output6= output6Font.render("Back", 2, (0,0,0))
                    sizeend=(840,640)
                    backgroundend = pygame.Surface(sizeend) #<-- like display, but creates a Surface object from scratch
                    backgroundend = backgroundend.convert() #<-- creates a copy of the Surface with a standard (faster)                            #    colour format
                    backgroundend.fill((0,0,0))
                    button1 =pygame.image.load(os.path.join(scriptDir,"img/button.png"))
                    button1=button1.convert_alpha()
                    button1 = pygame.transform.scale(button1, (140,55))
                    screen.blit(backgroundend,(0,0))

                    screen.blit(output2,(170,400))
                    screen.blit(output3,(150,100))
                    screen.blit(output4,(200,250))

                    screen.blit(button1,(200,500))
                    screen.blit(button1,(515,500))
                    screen.blit(output5,(225,515))
                    screen.blit(output6,(552,515))
                    pygame.display.flip()


        def reset():
            global startpoint
            global timepergrid
            global trainx
            global trainy
            startpoint=[28]
            trainx=530
            trainy=255
            timepergrid=1.0
            train.setimg(1)

        def instructions():
            clock = pygame.time.Clock() #<-- used to control the frame rate
            keep_going = True 	        #<-- a 'flag' variable for the game loop condition
            while keep_going:
                clock.tick(30)

                for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                        if ev.type == QUIT: #<-- this special event type happens when the window is closed
                            keep_going = False
                            pygame.mixer.music.stop()
                        elif ev.type == pygame.MOUSEBUTTONDOWN:
                            mousepos = pygame.mouse.get_pos()
                            x = mousepos[0]
                            y = mousepos[1]
                            if x>=720 and x<= 840 and y>=350 and y<=457:
                                keep_going=False
                                timereset(pygame.time.get_ticks())
                                main()

                            elif x>=720 and x<=840 and y>=500 and y<=607:
                                keep_going=False
                                startMenu()
                            elif x>=20 and x<=60 and y>=580 and y<=620:
                                sound.changeSetting()
                                sound.display()
                if keep_going==True:
                    output2Font = pygame.font.SysFont("How to play?", 75)
                    output2 = output2Font.render("How to play?", 2, (0,0,0))

                    output1Font = pygame.font.SysFont("Start Game",30)
                    output1 = output1Font.render("Click on the green grids to rotate the train tracks to connect them.", 2, (0,0,0))

                    output3Font = pygame.font.SysFont("How to play?",30)
                    output3 = output3Font.render("Note: You can only click on the ", 2, (0,0,0))

                    output4Font = pygame.font.SysFont("Settings",30)
                    output4 = output4Font.render("1. white grids", 2, (0,0,0))

                    output5Font = pygame.font.SysFont("Exit",30)
                    output5 = output5Font.render("2. the last clicked pink grid ", 2, (0,0,0))

                    output6Font = pygame.font.SysFont("Exit",55)

                    output6 = output5Font.render("3.the pink grid at the end of the connected path ", 2, (0,0,0))

                    output7 = output6Font.render("Play", 2, (255,255,255))
                    output8 = output6Font.render("Back", 2, (255,255,255))

                    demo = pygame.image.load(os.path.join(scriptDir,"img/demo.png")).convert_alpha()
                    demo= pygame.transform.scale(demo, (400,400))

                    button = pygame.image.load(os.path.join(scriptDir,"img/instruction_button.png")).convert_alpha()
                    button= pygame.transform.scale(button,(150,107))
                    pygame.display.set_caption("ChooChooTrain - How to play?")
                    sizeend=(840,640)
                    backgroundend = pygame.Surface(sizeend) #<-- like display, but creates a Surface object from scratch
                    backgroundend = backgroundend.convert() #<-- creates a copy of the Surface with a standard (faster)                            #    colour format
                    backgroundend.fill((0,0,0))
                    backimg= pygame.image.load(os.path.join(scriptDir,"img/instructions.jpg")).convert()
                    backimg = pygame.transform.scale(backimg, (840,640))
                    screen.blit(backgroundend,(0,0))
                    screen.blit(backimg,(0,0))
                    screen.blit(output2,(20,20))

                    screen.blit(output1,(50,80))
                    screen.blit(output3,(50,110))

                    screen.blit(output4,(100,140))
                    screen.blit(output5,(100,170))
                    screen.blit(output6,(100,200))
                    screen.blit(demo,(120,230))

                    screen.blit(button,(720,350))
                    screen.blit(output7,(740,380))

                    screen.blit(button,(720,500))
                    screen.blit(output8,(740,530))
                    sound.display()


                    pygame.display.flip()




        def startMenu():

            clock = pygame.time.Clock() #<-- used to control the frame rate
            keep_going = True 	        #<-- a 'flag' variable for the game loop condition


            while keep_going:

                clock.tick(30)

                for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                        if ev.type == QUIT: #<-- this special event type happens when the window is closed
                            keep_going = False
                            pygame.mixer.music.stop()
                        elif ev.type == pygame.MOUSEBUTTONDOWN:
                            mousepos = pygame.mouse.get_pos()
                            x = mousepos[0]
                            y = mousepos[1]
                            if x>=150 and x<= 350 and y>=200 and y<=367:
                                keep_going=False
                                timereset(pygame.time.get_ticks())
                                main()

                            elif x>=450 and x<=650 and y>=200 and y<=367:
                                keep_going=False
                                instructions()

                            elif x>=250 and x<= 450 and y>= 400 and y<= 567:
                                pygame.mixer.music.stop()
                                keep_going=False
                            elif x>=20 and x<=60 and y>=580 and y<=620:
                                sound.changeSetting()
                                sound.display()
                if keep_going==True:
                    output2Font = pygame.font.SysFont("Choo Choo Train", 100)
                    output2 = output2Font.render("Choo Choo Train", 2, (0,0,0))
                    output1Font = pygame.font.SysFont("Start Game",30)
                    output1 = output1Font.render("Start Game", 2, (0,0,0))

                    output3Font = pygame.font.SysFont("How to play?",30)
                    output3 = output3Font.render("How to play?", 2, (0,0,0))

                    output4Font = pygame.font.SysFont("Settings",30)
                    output4 = output4Font.render("Exit", 2, (0,0,0))

                    cloud = pygame.image.load(os.path.join(scriptDir,"img/cloud.png")).convert_alpha()
                    cloud = pygame.transform.scale(cloud, (200,167))

                    pygame.display.set_caption("ChooChooTrain")
                    sizeend=(840,640)
                    backgroundend = pygame.Surface(sizeend) #<-- like display, but creates a Surface object from scratch
                    backgroundend = backgroundend.convert() #<-- creates a copy of the Surface with a standard (faster)                            #    colour format
                    backgroundend.fill((0,0,0))
                    backimg= pygame.image.load(os.path.join(scriptDir,"img/station.jpg")).convert()
                    backimg = pygame.transform.scale(backimg, (840,640))


                    screen.blit(backgroundend,(0,0))
                    screen.blit(backimg,(0,0))
                    screen.blit(output2,(20,20))

                    screen.blit(cloud,(150,200))
                    screen.blit(output1,(205,275))

                    screen.blit(cloud,(450,200))
                    screen.blit(output3,(495,275))

                    screen.blit(cloud,(250,400))
                    screen.blit(output4,(320,475))

                    sound.display()

                    pygame.display.flip()


        def main():
            global startpoint
            global timepergrid
            global trainx
            global trainy
            global startpoint
            global click
            pygame.display.set_caption("ChooChooTrain") #<-- caption appears in the title bar
            sizeright=(640,640)
            backgroundr = pygame.Surface(sizeright) #<-- like display, but creates a Surface object from scratch
            backgroundr = backgroundr.convert() #<-- creates a copy of the Surface with a standard (faster)                            #    colour format
            backgroundr.fill((0, 0, 255)) #<-- fills Surface with colour using a tuple (red, green, blue).

            timeboxsize = (180,100)
            timebox = pygame.Surface(timeboxsize)
            timebox = timebox.convert()
            timebox.fill((0, 0, 0))

            img = pygame.image.load(os.path.join(scriptDir,"img/sky.jpg"))
            img = img.convert()
            img = pygame.transform.scale(img, (200,640))


            screen.blit(train.getimg(),(530,240))



            for i in range(64):
                    tempsc= set1[i]
                    trackgrid.append(Track(i,tempsc, 0, 0))
                    temporient=randint(0,3)
                    tempimg=trackgrid[i].getImage()
                    imgs.append(pygame.image.load(os.path.join(scriptDir,tempimg)))
                    imgs[i] = imgs[i].convert()
                    imgs[i] = pygame.transform.scale(imgs[i], (80,80))
                    y = (i/8)*80
                    x = (i%8)*80+200

                    screen.blit(imgs[i],(x,y))
                    if temporient!=0:
                        for a in range(temporient):
                            trackgrid[i].rotate()

            trackgrid[28].setWp(1)
            trackgrid[28].setOrient(1)



            for i in range(64):

                if findUnconnectedEnd(trackgrid[startpoint[-1]]) ==False:
                    break

            clock = pygame.time.Clock() #<-- used to control the frame rate
            keep_going = True 	        #<-- a 'flag' variable for the game loop condition
            counter=0
            counter1=0

            game_over=False

            while keep_going:

                clock.tick(30) #<-- Set a constant frame rate, argument is frames per second

                for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                    if ev.type == QUIT: #<-- this special event type happens when the window is closed
                        keep_going = False
                        pygame.mixer.music.stop()
                    elif ev.type == pygame.MOUSEBUTTONDOWN:
                        mousepos = pygame.mouse.get_pos()
                        x = mousepos[0]
                        y = mousepos[1]
                        if x>=200:
                            tracknum = (x-200)/80+ y/80*8
                        elif x>=20 and x<=60 and y>=580 and y<=620:
                            sound.changeSetting()
                            sound.display()
                            tracknum=65
                        else:
                            tracknum=65
                        if game_over==False:
                            try:
                                if trackgrid[tracknum].getLock()==False:

                                    trackgrid[tracknum].rotate()
                                    click.append(tracknum)
                                    try:

                                        changecolor(trackgrid[tracknum],startpoint[-1])

                                    except IndexError:
                                        changecolor(trackgrid[tracknum],28)
                                else:
                                    if trackgrid[tracknum].getLock()==True and click!=[] and click[-1]==tracknum and tracknum in startpoint:
                                        trackgrid[tracknum].setlock(False)
                                        trackgrid[tracknum].rotate()
                                        index=0
                                        for i in range (len(startpoint)):
                                            if startpoint[i]==tracknum:
                                                index = i
                                        for i in range (len(startpoint)):
                                            if i>index:
                                                trackgrid[startpoint[i]].setWp(0)
                                                trackgrid[startpoint[i]].setlock(False)
                                        startpoint = startpoint[:index]
                                        try:
                                            changecolor(trackgrid[tracknum],startpoint[-1])
                                        except IndexError:
                                            changecolor(trackgrid[tracknum],28)
                            except IndexError:
                                pass
                        else:
                            if x>=200 and x<=340 and y>=500 and y<=555:
                                main()

                if game_over==False:
                    time = pygame.time.get_ticks()-diff
                    min = time/60000
                    sec = (time-min*60000)/1000

                    if len(str(min))==1 and len(str(sec))==1:
                        stime = "0"+str(min)+":0"+str(sec)
                    elif len(str(min))==1 and len(str(sec))==2:
                        stime = "0"+str(min)+":"+str(sec)
                    elif len(str(min))==2 and len(str(sec))==1:
                        stime = str(min)+":0"+str(sec)

                    timefont = pygame.font.SysFont(str(stime), 75)
                    label = timefont.render(str(stime), 2, (255,255,0))
                    titletime=pygame.font.SysFont("TIME:", 75)
                    label2 = timefont.render("TIME:", 2, (255,255,0))

                    screen.blit(img,(0,0))
                    screen.blit(timebox,(10,20))
                    screen.blit(label, (35, 75))
                    screen.blit(label2, (35, 25))
                    sound.display()
                    for i in range(64):
                        y = (i/8)*80
                        x = (i%8)*80+200
                        screen.blit(imgs[i],(x,y))



                if sec>15 and sec<45 and game_over==False:
                    if trackgrid[grid[min]].getShowSpecial() == True:
                        trackgrid[grid[min]].setSpecial(gridtype[min])
                        screen.blit(specialpic[gridtype[min]],(trackgrid[grid[min]].getx()+25,trackgrid[grid[min]].gety()+10))

                try:
                    if time >3000:
                        temp1=setPos(startpoint[counter],counter)
                        trainx=setPos(startpoint[counter],counter)[0]
                        trainy=setPos(startpoint[counter],counter)[1]
                        counter1+=1

                        """if counter1%900==0:
                            timepergrid-=0.2
                            if timepergrid==0.0:
                                    timepergrid=0.5"""


                        if counter==0 and float(counter1/(15*timepergrid))==int(counter1/(15*timepergrid)):
                            trackgrid[startpoint[counter]].setWp(0)
                            trackgrid[startpoint[counter]].setOrient(randint(0,3))
                            trackgrid[startpoint[counter]].setlock(False)
                            counter+=1

                            if trackgrid[startpoint[counter]].getSpecial()==0:
                                timepergrid-=0.3
                                if timepergrid==0.0:
                                    timepergrid=0.5

                                trackgrid[startpoint[counter]].setSpecial(-1)
                                trackgrid[startpoint[counter]].setShowSpecial(False)
                            elif trackgrid[startpoint[counter]].getSpecial()==1:
                                timepergrid+=0.3

                                trackgrid[startpoint[counter]].setSpecial(-1)
                                trackgrid[startpoint[counter]].setShowSpecial(False)

                        if counter!=0 and float(counter1/(30*timepergrid))==int(counter1/(30*timepergrid)):
                            trackgrid[startpoint[counter]].setWp(0)
                            trackgrid[startpoint[counter]].setOrient(randint(0,3))
                            trackgrid[startpoint[counter]].setlock(False)
                            counter+=1

                            if trackgrid[startpoint[counter]].getSpecial()==0:
                                timepergrid-=0.3
                                if timepergrid==0.0:
                                    timepergrid=0.5
                                trackgrid[startpoint[counter]].setSpecial(-1)
                                trackgrid[startpoint[counter]].setShowSpecial(False)

                            elif trackgrid[startpoint[counter]].getSpecial()==1:
                                timepergrid+=0.3
                                trackgrid[startpoint[counter]].setSpecial(-1)
                                trackgrid[startpoint[counter]].setShowSpecial(False)

                except IndexError:
                    keep_going=False
                    game_over=True

                    endScreen(time)
                    updateDatabase()
                if game_over==False:
                    screen.blit(train.getimg(),(trainx-30,trainy-30))
                    screen.blit(train.getimg(),(trainx-30,trainy-30))
                    pygame.display.flip()

        startMenu()
        screen = pygame.display.set_mode(size2)

class Sound(ChooChooTrain):  #this class is used to control the backgroud music

    img="img/speaker.png"   #img controls the icon
    play=True           #this boolean controls whether the music is playing
    x = 20              # x and y are the postions of the music icon
    y = 580
    def changeSetting(self):    #changes the play-pause status of the music
        if self.play==True:
            self.play =False
            pygame.mixer.music.pause()  #pause the music
        else:
            self.play = True
            pygame.mixer.music.unpause()    #play the music


    def reset(self):    #resets the icon
        if self.play==True:
            self.img= "img/speaker.png"
        else:
            self.img = "img/mute.png"
    def getPlay(self):  #fetches the boolean
        return self.play
    def getx(self):     #returns x coordinate of the icon
        return self.x
    def gety(self):      #returns y coordinate of the icon
        return self.y
    def display(self):  #displays the music icon on screen
        self.reset()
        img = pygame.image.load(os.path.join(scriptDir,self.img)).convert_alpha()
        img = pygame.transform.scale(img,(40,40))
        screen.blit(img,(self.x,self.y))



class Train(ChooChooTrain):
    img=trainimg[0]
    def setimg(self,num):
        if num ==1:
            self.img=trainimg[0]
        elif num==2:
            self.img=trainimg[1]
        elif num==3:
            self.img=trainimg[2]
    def getimg(self):
        return self.img
sound=Sound()
train=Train()

class Track(ChooChooTrain):  #this class is used to control the track grids
    global screen
    sc=0
    number =0
    orient=0
    wp=0
    x=0
    y=0
    cons=1
    cont=1
    lock=False
    special=-1
    showspecial=True
    __image=""
    def __init__(self,number,sc,orient,wp):
        self.number=number
        self.orient = orient
        self.y = (number/8)*80
        self.x = (number%8)*80+200
        self.wp = wp
        self.sc=sc

        if self.sc ==0 and self.wp == 0:
            self.__image = "img/sw.png"
        elif self.sc ==0 and self.wp == 1:
            self.__image="img/sp.png"
        elif self.sc==1 and self.wp==0:
            self.__image = "img/cw.png"
            if self.orient == 0 :
                self.cons=1
                self.cont=1
            elif self.orient ==1:
                self.cons =0
                self.cont=1
            elif self.orient ==2:
                self.cons=0
                self.cont=0
            else:
                self.cons=1
                self.cont=0
        else:
            self.__image = "img/cp.png"
            if self.orient == 0 :
                self.cons=1
                self.cont=1
            elif self.orient ==1:
                self.cons =0
                self.cont=1
            elif self.orient ==2:
                self.cons=0
                self.cont=0
            else:
                self.cons=1
                self.cont=0


    def getImage(self): # return the image name
        return self.__image
    def getNumber(self):    #return the track number
        return self.number
    def getOrient(self):    #return the number that corresponds to the orientation
        return self.orient
    def rotate(self):       #rotate the grid
        self.orient +=1
        if self.orient ==4:
            self.orient =0

        if self.orient == 0 :
            self.cons=1
            self.cont=1
        elif self.orient ==1:
            self.cons =0
            self.cont=1
        elif self.orient ==2:
            self.cons=0
            self.cont=0
        else:
            self.cons=1
            self.cont=0
        imgs[self.number]=pygame.transform.rotate(imgs[self.number],-90)
        screen.blit(imgs[self.number],(self.x,self.y))

    def setOrient(self,o):  #reset the orientation
        self.orient = o
        self.resetImage()
        if self.orient == 0:
            self.cons=1
            self.cont=1
        elif self.orient ==1:
            self.cons =0
            self.cont=1
        elif self.orient ==2:
            self.cons=0
            self.cont=0
        else:
            self.cons=1
            self.cont=0
        imgs[self.number]=pygame.image.load(os.path.join(scriptDir,self.__image))
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        imgs[self.number]=pygame.transform.rotate(imgs[self.number],self.orient*(-90))
        screen.blit(imgs[self.number],(self.x,self.y))

    def setSc(self,o):  #set straight or curve
        self.sc =o
        self.resetImage()
        imgs[self.number]=pygame.image.load(os.path.join(scriptDir,self.__image))
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        screen.blit(imgs[self.number],(self.x,self.y))

    def setWp(self,color):  #set the colour of the grid
        self.wp=color
        self.resetImage()
        imgs[self.number]=pygame.image.load(os.path.join(scriptDir,self.__image))
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        imgs[self.number]=pygame.transform.rotate(imgs[self.number],self.orient*(-90))
        screen.blit(imgs[self.number],(self.x,self.y))
    def resetImage(self):   # updates the colour and type of the train track
        if self.sc ==0 and self.wp == 0:
            self.__image = "img/sw.png"
        elif self.sc ==0 and self.wp == 1:
            self.__image="img/sp.png"
        elif self.sc==1 and self.wp==0:
            self.__image = "img/cw.png"
        elif self.sc==1 and self.wp==1:
            self.__image = "img/cp.png"
    def getWp(self):    #returns the colour of the track
        return self.wp
    def getSc(self):    #returns the tpe of the track
        return self.sc
    def getCont(self):  #returns whether the track connects to the top or bottom edge of the grid
        return self.cont
    def getCons(self):  #returns whether the track connects to the side edges of the grid
        return self.cons
    def setlock(self,btf):  #set a lock on the track grid so that the user cannot click on it
        self.lock=btf
    def getLock(self):      #returns whether a lock is put on the track
        return self.lock
    def getx(self):     #returns the x-coordinate of the grid
        return self.x
    def gety(self):     #returns the y-coordinate of the grid
        return self.y
    def getSpecial(self):   #returns whether a special item is on the grid
        return self.special
    def setSpecial(self,sp):    #set a special item on a grid
        self.special=sp
    def getShowSpecial(self):
        return self.showspecial
    def setShowSpecial(self,btf):
        self.showspecial=btf


