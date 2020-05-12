#CoronaGame
import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
from pygame.transform import rotate,scale
from os.path import join
from random import randint as ri
from time import sleep


#OPENCV DECLARATIONS
camera = cv2.VideoCapture(0)
_,frame=camera.read()


#Setting window size according to camera frame
lengthCameraFrame=np.shape(frame)[1] 
widthCameraFrame=np.shape(frame)[0]
pygame.init()
pygame.display.set_caption("Fight Corona")
screen = pygame.display.set_mode([lengthCameraFrame+widthCameraFrame,widthCameraFrame])



#Pygame Variables
HeightField=240
HeightGround=widthCameraFrame-HeightField
#CharPath="G:\Fight_Corona\dino_game\trexfile\trex\graphics_files"
VirusVelocity=20 #20 pixels/sec
afterLoop=0
isJump = False
isCrouch=False
jumpCount = 7
obstacleNumber=[0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3] #This matrix defines number of obstacle you may edit the numbers
#The more the numbers will appear, the higher will be the probability of the obstacle to appear
#Here the probability of 1 obstacle is 7/20
obstacleType=[0,0,0,0,0,0,1,1,1,2] #0=> Land obstacle 1=> Fly obstacle 2=>Remedie
xV=lengthCameraFrame+widthCameraFrame
JumpStage=False
JumpMagnitude=jumpCount
run = True
x=50
y=0
abortJump=False
afterLoop=1
SkyClear=1
#######################Game Variables######################
xV=lengthCameraFrame+widthCameraFrame
SkyX=lengthCameraFrame+widthCameraFrame
SkyVelocity=25
SkyLoop=1
topThresh=20
bottomThresh=10
xHome=lengthCameraFrame+widthCameraFrame
bendFunc=False
GameLives=3
sPC=-1
##############################################Game Character Moves#####################################


CharacterActions=[] #0-Normal movement 1-Jump 2-Bend
CharSize=75
charrot=-90
CharacterActions.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\character.png"),(CharSize,CharSize)))
CharacterActions.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\jumpC.png"),(CharSize,CharSize)))
#This is special case of bending, if you want to modify make changes accordingly Aspect ratio must be 64:46
CharacterActions.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\bendC.png"),(64,46)))



###############################################Land Virus##############################################


Viruses=[]
virussize=60
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv1.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv2.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv3.png"),(89,59))) #Long Sized Virus
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv4.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv5.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv6.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv7.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv8.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv9.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv10.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv11.png"),(virussize,virussize)))
Viruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv12.png"),(virussize,virussize)))
#Add your virus characters here if you want but make sure that it's yCod is accordingly adjusted in Incoming() function

################################################Air Viruses##########################################


FlyViruses=[]
flyvirussize=80 #Aspect ratio is 2:1
FlyViruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\fly1.png"),(flyvirussize,int(flyvirussize/2))))
FlyViruses.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\fly2.png"),(flyvirussize,int(flyvirussize/2))))


########################################################Remedies#################################################


Remedies=[]
SanetizerBottleSize=60 #Aspect Ratio: 3:5
HomeSize=80
ExplosionSize=50
Remedies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizer.png"),(SanetizerBottleSize,int(5*SanetizerBottleSize/3))))
Remedies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\home.png"),(HomeSize,HomeSize)))
Remedies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\explosion.png"),(ExplosionSize,ExplosionSize)))
Remedies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\whiteSmoke.png"),(ExplosionSize,ExplosionSize)))


######################################################################################################################

#######################################Sky Propogation##########################################################


CloudLength=80
CloudWidth=30
BirdSquare=50
BirdRectangleH=60
BirdRectangleW=40
Skies=[]
Skies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cloud.png"),(CloudLength,CloudWidth)))
Skies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cloud2.png"),(CloudLength,CloudWidth)))
Skies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\bird1.png"),(BirdRectangleH,BirdRectangleW)))
Skies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\bird2.png"),(BirdRectangleH,BirdRectangleW)))
Skies.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\bird3.png"),(BirdSquare,BirdSquare)))


#############################################################################################################
####################################Game Graphics##############################################################

ExitScreen=scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\FinalScreen.png"),(widthCameraFrame,widthCameraFrame))
GroundScreen=scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\Ground.png"),(widthCameraFrame,int(widthCameraFrame/2)))
SkyScreen=scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\SkyScreen.png"),(widthCameraFrame,int(widthCameraFrame/2)))
HomeReach=scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\ReachedHome.png"),(widthCameraFrame,widthCameraFrame))
SanProt=[] #Sanetizer Protection BGs
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection1.png"),(widthCameraFrame,int(widthCameraFrame/2))))
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection2.png"),(widthCameraFrame,int(widthCameraFrame/2))))
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection3.png"),(widthCameraFrame,int(widthCameraFrame/2))))

####################################Game Graphics##############################################################

def ChooseVirus():
    fly=ri(0,1)
    vs=virussize
    if fly:
        virus=FlyViruses[ri(0,len(FlyViruses)-1)]
        vs=int(flyvirussize/2)
    else:
        virusInd=ri(0,len(Viruses)-1)
        if virusInd==2:
            vs=59
        virus=Viruses[virusInd]
        
    return([virus,vs])
def VirusCod(xV):
    afterLoop=0
    xV-=VirusVelocity
    virusTerminates=False
    if  xV<=lengthCameraFrame:
        xV=lengthCameraFrame+widthCameraFrame
        afterLoop=1
    return(xV,afterLoop)
#Uncomment the code below to check for the visualizations of your characters ig you raise number of characters you have to change the loop ranges
'''
print(f"Total Moves:- {len(CharacterActions)}, Total Land Virus:- {len(Viruses)}, Total Air Viruses:- {len(FlyViruses)}, Total Remedies:- {len(Remedies)}")
temp=100
for i in range(3):
    screen.blit(CharacterActions[i],(temp*i,10))
temp=80
for j in range(9):
    screen.blit(Viruses[j],(temp*j,110))
temp=100
for k in range(2):
    screen.blit(FlyViruses[k],(temp*k,210))
temp=100
for l in range(3):
    screen.blit(Remedies[l],(temp*l,300))
pygame.display.update()
#Game
'''
def Incoming(): #Function to initiate virus movement
    xTest=lengthCameraFrame+widthCameraFrame+400
    yCodT=virussize
    choose=obstacleType[ri(0,len(obstacleType)-1)]
    if choose==0:
        vindex=ri(0,len(Viruses)-1)
        testVirus=Viruses[vindex]
        if vindex==2:
            vs=46
        else:vs=virussize
        yCodT=int(widthCameraFrame/2)-vs
        yCodB=0
    elif choose==1:
        testVirus=FlyViruses[ri(0,len(FlyViruses)-1)]
        yCodT=int(widthCameraFrame/2)-(CharSize)-15
        yCodB=0
    else:
        testVirus=Remedies[0]
        yCodT=int(widthCameraFrame/2)-int(5*SanetizerBottleSize/3)
        yCodB=1
        print(yCodB)
    return(testVirus,yCodT,yCodB)
def SkyPropogate():
    Index=ri(0,len(Skies)-1)
    SkyEntity=Skies[Index]
    yC=30
    return(SkyEntity,yC)


def SkyCod(xV):
    SkyLoop=0
    xV-=SkyVelocity
    if  xV<=lengthCameraFrame:
        xV=lengthCameraFrame+widthCameraFrame
        SkyLoop=1
    return(xV,SkyLoop)

def GoExplosion(y1,z1):
    z1-=1
    screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(GroundScreen,(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(Remedies[2], (lengthCameraFrame+x,y1))
    pygame.display.update()
    sleep(1.5)
    return(z1)
def GameOverScreen():
    screen.blit(ExitScreen,(lengthCameraFrame,0))
    pygame.display.update()
    sleep(4)
def HomeReachScreen():
    screen.blit(HomeReach,(lengthCameraFrame,0))
    pygame.display.update()
    sleep(8)
def SanetizerProtection(x1,y1,z1):
    screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(SanProt[2-z1],(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(CharacterActions[0],(lengthCameraFrame+x, int(widthCameraFrame/2)+y-CharSize))
    screen.blit(Remedies[3], (x1,y1))
    pygame.display.update()
    sleep(1)


#Real time processing

while run:
    if afterLoop==1:
        testVirus,yCod,yCodB=Incoming()
        if yCodB==1:
            yCod=int(widthCameraFrame/2)-(CharSize)-15
            sPC=2
        afterLoop=0
    _,frame=camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    pygame.time.delay(100)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if not(isJump): 
        if keys[pygame.K_SPACE]:
            isJump = True
        elif keys[pygame.K_UP]:
            isCrouch=True
    else:
        if keys[pygame.K_UP]:
            isCrouch=True
            abortJump=True
        elif jumpCount >= -1*JumpMagnitude:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            jumpCount = JumpMagnitude
            isJump = False
    if int(widthCameraFrame/2)+y>int(widthCameraFrame/2):
        y=0
    screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(GroundScreen,(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))  
    if isJump:
        if not(abortJump):
            screen.blit(CharacterActions[1],(lengthCameraFrame+x, int(widthCameraFrame/2)+y-CharSize)) #Do it - for crouch
        else:
           screen.blit(CharacterActions[2],(lengthCameraFrame+x, int(widthCameraFrame/2)-46))
           abortJump=False
           isCrouch=True
           isJump=False
           jumpCount=JumpMagnitude
    elif isCrouch:
        screen.blit(CharacterActions[2],(lengthCameraFrame+x, int(widthCameraFrame/2)-46))
        isCrouch=False
        bendFunc=True
        y=0
    else:
        screen.blit(CharacterActions[0],(lengthCameraFrame+x, int(widthCameraFrame/2)+y-CharSize))  
    xV,afterLoop=VirusCod(xV)
    yPlayerTop=int(widthCameraFrame/2)+y-CharSize
    yPlayerBottom=int(widthCameraFrame/2)+y
    if xV>=lengthCameraFrame+x and xV<=lengthCameraFrame+x+CharSize:
        if bendFunc:
            yPlayerTop=int(widthCameraFrame/2)-46
            if yCod>=yPlayerTop-topThresh and yCod<=yPlayerBottom-bottomThresh:
                if sPC>=0:
                    y=0
                    SanetizerProtection(xV,yCod,sPC)
                    sPC-=1
                    xV=lengthCameraFrame+widthCameraFrame
                    testVirus,yCod,yCodB=Incoming()
                else:
                    GameLives=GoExplosion(yPlayerTop,GameLives)
                    y=0
                    isJump=False
                    jumpCount=JumpMagnitude
                    if GameLives<=0:
                        GameOverScreen()
                        break
                    xV=lengthCameraFrame+widthCameraFrame
                    testVirus,yCod,yCodB=Incoming()
                bendFunc=False
        else:
            if yCod>=yPlayerTop-topThresh and yCod<=yPlayerBottom-bottomThresh:
                if sPC>=0:
                    SanetizerProtection(xV,yCod,sPC)
                    sPC-=1
                    y=0
                    xV=lengthCameraFrame+widthCameraFrame
                    testVirus,yCod,yCodB=Incoming()
                else:
                    GameLives=GoExplosion(yPlayerTop,GameLives)
                    y=0
                    isJump=False
                    jumpCount=JumpMagnitude
                    if GameLives<=0:
                        GameOverScreen()
                        break
                    xV=lengthCameraFrame+widthCameraFrame
                    testVirus,yCod,yCodB=Incoming()
    if SkyLoop==1:
        SkyE,SkyY=SkyPropogate()
        SkyLoop=0
    SkyX,SkyLoop=SkyCod(SkyX)
    screen.blit(SkyE,(SkyX, SkyY))
    screen.blit(testVirus,(xV, yCod))
    pygame.display.update()
    if pygame.time.get_ticks()>=60000:
        screen.blit(Remedies[1],(xHome, int(widthCameraFrame/2)-HomeSize))
        while xHome>=lengthCameraFrame+x:
            xHome,_=VirusCod(xHome)
            sleep(0.1)
            screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
            screen.blit(GroundScreen,(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
            screen.blit(CharacterActions[0],(lengthCameraFrame+x, int(widthCameraFrame/2)-CharSize))
            screen.blit(Remedies[1],(xHome, int(widthCameraFrame/2)-HomeSize))
            pygame.display.update()
        screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
        screen.blit(GroundScreen,(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
        screen.blit(Remedies[1],(xHome, int(widthCameraFrame/2)-HomeSize))
        pygame.display.update()
        sleep(2)
        HomeReachScreen()
        break
    
pygame.quit()
