import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
from pygame.transform import rotate
def convertToRGB(image,sizex,sizey):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    resize=cv2.resize(image,(sizex,sizey),interpolation=cv2.INTER_CUBIC)
    return(resize)

#OPENCV DECLARATIONS
camera = cv2.VideoCapture(0)
_,frame=camera.read()
#Setting window size according to camera frame
lengthCameraFrame=np.shape(frame)[1] 
widthCameraFrame=np.shape(frame)[0]
pygame.init()
pygame.display.set_caption("T-Rex Runner")
screen = pygame.display.set_mode([lengthCameraFrame+widthCameraFrame,widthCameraFrame])



#Pygame Variables
HeightField=240
HeightGround=widthCameraFrame-HeightField
colorEnvironment=(49,139,186) #in RGB Format
colorGround=(44,175,30) #in RGB Format


#Image Variables
CharacterImage=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files/character.png")
CharacterJump=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files/jumpC.png")
CharacterBend=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files/bendC.png")


LandVirus1=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv1.png")
LandVirus2=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv2.png")
LandVirus3=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv3.png")
LandVirus4=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv4.png")
LandVirus5=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv5.png")
LandVirus6=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv6.png")
LandVirus7=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv7.png")
LandVirus8=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv8.png")
LandVirus9=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\cv9.png")

FlyVirus1=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\fly1.png")
FlyVirus2=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\fly2.png")

Sanetizer=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizer.png")
Home=cv2.imread(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\home.png")
#Environment Settings
#character=pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files/character.png") For direct loading
velocity=5
jumpHeight=20
x=lengthCameraFrame
y=HeightField

#Converting to surfaces

#########Character###############################
CharacterActions=[] #0-Normal movement 1-Jump 2-Bend
CharSize=75
charrot=-90
CharacterImage=convertToRGB(CharacterImage,CharSize,CharSize)
CharacterActions.append(rotate(pygame.surfarray.make_surface(CharacterImage),charrot).convert_alpha())
CharacterJump=convertToRGB(CharacterJump,CharSize,CharSize)
CharacterActions.append(rotate(pygame.surfarray.make_surface(CharacterJump),charrot))
CharacterBend=convertToRGB(CharacterBend,64,46) #This is special case of bending, if you want to modify make changes accordingly
CharacterActions.append(rotate(pygame.surfarray.make_surface(CharacterBend),charrot))
######################################################
###################Land_Virus Here you can add your own villians##########################
Viruses=[]
virussize=60
LandVirus1=convertToRGB(LandVirus1,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus1),-90))
LandVirus2=convertToRGB(LandVirus2,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus2),-90))
LandVirus3=convertToRGB(LandVirus3,89,59) #This is a special case of wide virus, if you want to increase width accordingly adjust this
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus3),-90))
LandVirus4=convertToRGB(LandVirus4,virussize,virussize) 
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus4),-90))
LandVirus5=convertToRGB(LandVirus5,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus5),-90))
LandVirus6=convertToRGB(LandVirus6,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus6),-90))
LandVirus7=convertToRGB(LandVirus7,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus7),-90))
LandVirus8=convertToRGB(LandVirus8,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus8),-90))
LandVirus9=convertToRGB(LandVirus9,virussize,virussize)
Viruses.append(rotate(pygame.surfarray.make_surface(LandVirus9),-90))

##########Fly Viruses ######################
FlyViruses=[]
flyvirussize=80 #Aspect ratio is 2:1
FlyVirus1=convertToRGB(FlyVirus1,flyvirussize,int(flyvirussize/2))
FlyViruses.append(rotate(pygame.surfarray.make_surface(FlyVirus1),-90))
FlyVirus2=convertToRGB(FlyVirus2,flyvirussize,int(flyvirussize/2))
FlyViruses.append(rotate(pygame.surfarray.make_surface(FlyVirus2),-90))

###################Remedies####################
Remedies=[]
SanetizerBottleSize=60 #Aspect Ratio: 3:5
HomeSize=80
ExplosionSize=50
Sanetizer=convertToRGB(Sanetizer,SanetizerBottleSize,int(5*SanetizerBottleSize/3))
Remedies.append(rotate(pygame.surfarray.make_surface(Sanetizer),-90))
Home=convertToRGB(Home,HomeSize,int(5*HomeSize/3))
Remedies.append(rotate(pygame.surfarray.make_surface(Home),-90))
Explosion=convertToRGB(Home,ExplosionSize,ExplosionSize)
Remedies.append(rotate(pygame.surfarray.make_surface(Explosion),-90))
###########Testing Visualization of the characters###############
#Uncomment the code below to check for the visualizations of your characters
'''
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
for l in range(2):
    screen.blit(Remedies[l],(temp*l,300))
pygame.display.update()
#Game
'''
#######################################################
try:
    while True:
        ret, frame = camera.read()               
        screen.fill([0,0,0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        for event in pygame.event.get():
##            if event.type == KEYDOWN:
##                sys.exit(0)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x-=velocity
            elif keys[pygame.K_RIGHT]:
                x+=velocity
        pygame.draw.rect(screen,colorEnvironment,(lengthCameraFrame,0,widthCameraFrame,HeightField))
        pygame.draw.rect(screen,colorGround,(lengthCameraFrame,HeightField,widthCameraFrame,HeightGround))
        screen.blit(CharacterActions[0],(x,HeightField-CharSize))
        #screen.blit(jumpC,(lengthCameraFrame+100,HeightField-100))
        #screen.blit(bendC,(lengthCameraFrame+200,HeightField-100))
        pygame.display.update()
except KeyboardInterrupt:
    pygame.quit()
    cv2.destroyAllWindows()

