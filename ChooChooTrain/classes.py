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

class sound():  #this class is used to control the backgroud music
    img="speaker.png"   #img controls the icon
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
            self.img= "speaker.png"
        else:
            self.img = "mute.png"
    def getPlay(self):  #fetches the boolean
        return self.play
    def getx(self):     #returns x coordinate of the icon
        return self.x
    def gety(self):      #returns y coordinate of the icon
        return self.y
    def display(self):  #displays the music icon on screen
        self.reset()
        img = pygame.image.load(self.img).convert_alpha()
        img = pygame.transform.scale(img,(40,40))
        screen.blit(img,(self.x,self.y))
class Track():  #this class is used to control the track grids
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
            self.__image = "sw.png"
        elif self.sc ==0 and self.wp == 1:
            self.__image="sp.png"
        elif self.sc==1 and self.wp==0:
            self.__image = "cw.png"
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
            self.__image = "cp.png"
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
        imgs[self.number]=pygame.image.load(self.__image)
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        imgs[self.number]=pygame.transform.rotate(imgs[self.number],self.orient*(-90))
        screen.blit(imgs[self.number],(self.x,self.y))

    def setSc(self,o):  #set straight or curve
        self.sc =o
        self.resetImage()
        imgs[self.number]=pygame.image.load(self.__image)
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        screen.blit(imgs[self.number],(self.x,self.y))

    def setWp(self,color):  #set the colour of the grid
        self.wp=color
        self.resetImage()
        imgs[self.number]=pygame.image.load(self.__image)
        imgs[self.number] = pygame.transform.scale(imgs[self.number], (80,80))
        imgs[self.number]=pygame.transform.rotate(imgs[self.number],self.orient*(-90))
        screen.blit(imgs[self.number],(self.x,self.y))

    def resetImage(self):   # updates the colour and type of the train track
        if self.sc ==0 and self.wp == 0:
            self.__image = "sw.png"
        elif self.sc ==0 and self.wp == 1:
            self.__image="sp.png"
        elif self.sc==1 and self.wp==0:
            self.__image = "cw.png"
        elif self.sc==1 and self.wp==1:
            self.__image = "cp.png"
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



class Train():
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
