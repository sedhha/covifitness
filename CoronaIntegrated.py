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
threshold_pixels=2000
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
def calibrate_background():
    humanFound=False
    print("Calibrating... don't move!")
    sleep(5)
    for i in range(100):
        _,_=camera.read()
    _,bg=camera.read()
    gray=cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
    while not(humanFound):
        _,fm=camera.read()
        fm=cv2.GaussianBlur(fm,(3,3),0)
        gray=cv2.cvtColor(fm,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces)>1:
            print("Only one person at a time!")
        elif len(faces)==1:
            print("Background calibration successful, now adjust the height, by pressing the green button at top!")
            print("Left Button to reduce height and right to increase, press both together to complete calibration.")
            bg=fm
            humanFound=True
            break
        else:
            print("Trying to detect face.")
    
    heightCalibration=False
    _,fm=camera.read()
    fm=cv2.GaussianBlur(fm,(3,3),0)
    height,width,_=np.shape(fm)
    bg1=fm.copy()
    cv2.circle(fm, (int(width/10),int(height/4)), 50, (0,255,0), cv2.FILLED)
    cv2.circle(fm, (int(9*width/10),int(height/4)), 50, (0,255,0), cv2.FILLED)
    #cv2.rectangle(fm, (int(width/10)-50,int(height/4)-50), (int(width/10)+50,int(height/4)+50), (0,0,255), 1)
    #cv2.rectangle(fm, (int(9*width/10)-50,int(height/4)-50), (int(9*width/10)+50,int(height/4)+50), (0,0,255), 1)
    #bg1=fm.copy()
    print("Stay still!")
    sleep(2)
    sumU=7
    while not(heightCalibration):
        _,fm=camera.read()
        line_range=[float(1/3),float(1/4),float(1/5),float(1/6),float(1/7),float(1/8),float(1/9)]
        cv2.imshow("Orignal",fm)
        fm=cv2.GaussianBlur(fm,(3,3),0)
        fm1=fm.copy()
        cv2.rectangle(fm1, (int(width/10)-50,int(height/4)-50), (int(width/10)+50,int(height/4)+50), (0,0,255), 1)
        cv2.rectangle(fm1, (int(9*width/10)-50,int(height/4)-50), (int(9*width/10)+50,int(height/4)+50), (0,0,255), 1)
        subtraction=cv2.cvtColor(cv2.absdiff(fm,bg1),cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Calibration",subtraction)
        _,thresh1 = cv2.threshold(subtraction,20,255,cv2.THRESH_BINARY)
        cv2.imshow("fm",thresh1)
        left_button=thresh1[int(height/4)-50:int(height/4)+50,int(width/10)-50:int(width/10)+50]
        #print(f"Left frame count: {cv2.countNonZero(left_button)}")
        right_button=thresh1[int(height/4)-50:int(height/4)+50,int(9*width/10)-50:int(9*width/10)+50]
        #print(f"Right frame count: {cv2.countNonZero(right_button)}")
        if cv2.countNonZero(left_button)>=threshold_pixels:
            if cv2.countNonZero(right_button)>=threshold_pixels:
                #print("Both buttons pressed")
                #print("Calibration complete")
                jumpHeight=(width*line_range[sumU])
                #print(f"Top Height: {(width*line_range[sumU])}")
                break
            else:
                #cv2.line(fm1, (0,int(width*line_range[sumU])), (width,int(width*line_range[sumU])), (255,0,0), 2)
                sumU=sumU-1
                if sumU<0:
                    sumU=0
                #print(f"Right Button@ {sumU}")
                cv2.line(fm1, (0,int(width*line_range[sumU])), (width,int(width*line_range[sumU])), (255,0,0), 2)
                #cv2.imshow("fF",fm1)
                sleep(1)
        elif cv2.countNonZero(right_button)>=threshold_pixels:
            sumU=sumU+1
            if sumU>len(line_range)-1:
                sumU=len(line_range)-1
            #print(f"Left button pressed @ {sumU}")
            cv2.line(fm1, (0,int(width*line_range[sumU])), (width,int(width*line_range[sumU])), (255,0,0), 2)
            #cv2.imshow("fF",fm1)
            sleep(1)
            #cv2.line(fm1, (0,int(width*line_range[sumU])), (width,int(width*line_range[sumU])), (255,0,0), 2)
            #cv2.imshow("Ff",fm1)
        else:
            pass
            #print("No action")
        cv2.circle(fm, (int(width/10),int(height/4)), 50, (0,255,0), cv2.FILLED)
        cv2.circle(fm, (int(9*width/10),int(height/4)), 50, (0,255,0), cv2.FILLED)
        #cv2.imshow("Left+Right",np.hstack((left_button,right_button)))
        left_frame=thresh1[:,0:int(width/2)]
        right_frame=thresh1[:,int(width/2):width]
        k=cv2.waitKey(1)
        cv2.imshow("Ff",fm1)
        if k & 0xFF==ord('q'):
            break
    return(bg,jumpHeight)
bg,jH=calibrate_background()
print("Calibration Success")
cv2.destroyAllWindows()
jumpS=0
_,fm=camera.read()
cv2.imshow("Display",fm)
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
VirusVelocity=30 #20 pixels/sec
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
TimeofGame=120 #in Seconds
#######################Game Variables######################
xV=lengthCameraFrame+widthCameraFrame
SkyX=lengthCameraFrame+widthCameraFrame
SkyVelocity=45
SkyLoop=1
topThresh=20
bottomThresh=10
xHome=lengthCameraFrame+widthCameraFrame
bendFunc=False
GameLives=3
sPC=-1
TimeofGame=180
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
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection3.png"),(widthCameraFrame,int(widthCameraFrame/2))))
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection2.png"),(widthCameraFrame,int(widthCameraFrame/2))))
SanProt.append(scale(pygame.image.load(r"G:\Fight_Corona\dino_game\completeTrex\trex\graphics_files\sanetizerprotection1.png"),(widthCameraFrame,int(widthCameraFrame/2))))

####################################Game Graphics##############################################################

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
##def Incoming(): #Function to initiate virus movement
##    xTest=lengthCameraFrame+widthCameraFrame+400
##    yCodT=virussize
##    choose=obstacleType[ri(0,len(obstacleType)-1)]
##    if choose==0:
##        vindex=ri(0,len(Viruses)-1)
##        testVirus=Viruses[vindex]
##        if vindex==2:
##            vs=46
##        else:vs=virussize
##        yCodT=int(widthCameraFrame/2)-vs
##        yCodB=0
##    elif choose==1:
##        testVirus=FlyViruses[ri(0,len(FlyViruses)-1)]
##        yCodT=int(widthCameraFrame/2)-(CharSize)
##        yCodB=0
##    else:
##        testVirus=Remedies[0]
##        yCodT=int(widthCameraFrame/2)-int(5*SanetizerBottleSize/3)
##        yCodB=1
##        print(yCodB)
##    return(testVirus,yCodT,yCodB)
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

#Real time processing
direction=1
jumpMag=7
jumpGrowth=0.35
jumpLim=jumpMag
flagJ=0
flagC=0
EnemyPass=True
FlyVirusHeightTH=50
def reinitialize():
    return(lengthCameraFrame+widthCameraFrame+400,0,jumpMag)
ObstacleX,_,_=reinitialize()
def CharacterJump(y,jumpLim,flag):
    if jumpLim==-jumpMag:
        jumpLim=jumpMag
        y=0
        flag=0
    else:
        y+=jumpLim*abs(jumpLim)*jumpGrowth
        jumpLim-=1
    #print(f"Jump values:{jumpLim}")
    return(y,jumpLim,flag)

def GetObstacle():
    DangerOn=1
    if ri(0,9)==8: #Making an unlikely event
        VirusType=Remedies[0]
        VirusY=int(widthCameraFrame/2)-int(5*SanetizerBottleSize/3)
        DangerOn=0
        VType=0 #Bottle Type
    else:
        if ri(0,1):
            VirusType=Viruses[ri(0,len(Viruses)-1)]
            if Viruses.index(VirusType)==2:
                VirusY=int(widthCameraFrame/2)-59 #Special Case
                VType=1 #Special Virus Case
            else:
                VirusY=int(widthCameraFrame/2)-virussize
                VType=2 # General Viruses
        else:
            VirusType=FlyViruses[ri(0,len(FlyViruses)-1)]
            VirusY=int(widthCameraFrame/2)-int(flyvirussize/2)-FlyVirusHeightTH
            VType=3 #Flyinh
    return(VirusType,VirusY,DangerOn,VType)
CollisionYT=20
CollisionXT=20
SanetizerLife=0
def DetectCollision(Col_X1,Col_Y1,Col_X2,Col_Y2,Col_XX,Col_YY,DangerOn):
    if DangerOn:
        if Col_XX>=Col_X1 and Col_XX<=Col_X2:
            if Col_YY>=Col_Y1 and Col_YY<=Col_Y2:
                return(1)
            else:return(False)
        else:return(False)
    else:
        if Col_XX>=Col_X1 and Col_XX<=Col_X2:
            if Col_YY>=Col_Y1 and Col_YY<=Col_Y2:
                return(2)
            else:return(False)
        else:return(False)
    
def DrawFunction(screen,xC,yC,x1,y1,color=[255,0,0]):
    pygame.draw.rect(screen, color, [xC, yC, x1, y1], 1)
    
def DetectVirusWidth(index):
    if index==0:
        x=SanetizerBottleSize
        y=int(5*SanetizerBottleSize/3)
    elif index==1:
        x=89
        y=59
    elif index==2:
        x=virussize
        y=virussize
    elif index==3:
        x=flyvirussize
        y=int(flyvirussize/2)
    return(x,y)
cv2.destroyAllWindows()
def BoomVirus(screen,yy,yyy,x1,y1,ind):
    screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(SanProt[ind-1],(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(CharacterActions[0],(lengthCameraFrame+x, int(widthCameraFrame/2)-y-CharSize))
    screen.blit(Remedies[3], (lengthCameraFrame+x+70,y1-50))
    pygame.display.update()
    sleep(1.5)
while run:
    #Camera Display
    for i in range(3):
        _,fm=camera.read()
        img=fm.copy()
        k=cv2.waitKey(1)
        #fm=cv2.GaussianBlur(fm,(3,3),0)
        gray=cv2.cvtColor(fm,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces)==0:
            #print("This executes")
            jumpS=1
            break
        for (x_x,y_y,w_w,h_h) in faces:
            img = cv2.rectangle(img,(x_x,y_y),(x_x+w_w,y_y+h_h),(255,0,0),2)
            #print(f"Current Height:- {y+int(h/2)} vs required: {jH}")
            #roi_gray = gray[y:y+h, x:x+w]
    frame = cv2.cvtColor(fm, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    #pygame.time.delay(100)
##    if jumpS:
##        print("Jumping")
##        jumpS=0
##    else:
##        if (y_y+int(h_h/2))<jH:
##            pass
##            print("Running")
##        else:
##            print("Crouching")
##            #sleep(0.1)
##            #print("Bending")
##    #Game Settings
    if EnemyPass:
        Obstacle,ObstacleY,DangerOn,VType=GetObstacle()
        VirusWidthX,VirusWidthY=DetectVirusWidth(VType)
        EnemyPass=False
    
    keys = pygame.key.get_pressed()  
    yPlayerTop=int(widthCameraFrame/2)+y-CharSize
    yPlayerBottom=int(widthCameraFrame/2)+y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_SPACE] or jumpS:
        flagJ=1
        jumpS=0
    elif keys[pygame.K_UP] or (y_y+int(h_h/2))>jH:
        flagJ=0
        flagC=1
        y=0
        jumpLim=jumpMag
    screen.blit(SkyScreen,(lengthCameraFrame,0,widthCameraFrame,int(widthCameraFrame/2)))
    screen.blit(GroundScreen,(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))  
    if flagJ:
        y,jumpLim,flagJ=CharacterJump(y,jumpLim,flagJ)
        yPlayerTop=int(widthCameraFrame/2)+y-CharSize
        yPlayerBottom=int(widthCameraFrame/2)+y
        #print(yPlayerTop-topThresh,yPlayerBottom-bottomThresh)
        screen.blit(CharacterActions[1],(lengthCameraFrame+x, int(widthCameraFrame/2)-y-CharSize))
        #DrawFunction(screen,lengthCameraFrame+x,int(widthCameraFrame/2)-y-CharSize,CharSize,CharSize)
        Col_X1=lengthCameraFrame+x
        Col_X2=lengthCameraFrame+x+CharSize
        Col_Y1=int(widthCameraFrame/2)-y-CharSize
        Col_Y2=int(widthCameraFrame/2)-y
    elif flagC:
        yPlayerTop=int(widthCameraFrame/2)-46
        yPlayerBottom=int(widthCameraFrame/2)+y
        screen.blit(CharacterActions[2],(lengthCameraFrame+x, int(widthCameraFrame/2)-46))
        flagC=0
        #DrawFunction(screen,lengthCameraFrame+x,int(widthCameraFrame/2)-y-46,74,46)
        Col_X1=lengthCameraFrame+x
        Col_X2=lengthCameraFrame+x+74
        Col_Y1=int(widthCameraFrame/2)-y-46
        Col_Y2=int(widthCameraFrame/2)-y
    else:
        screen.blit(CharacterActions[0],(lengthCameraFrame+x, int(widthCameraFrame/2)-y-CharSize))
        #DrawFunction(screen,lengthCameraFrame+x,int(widthCameraFrame/2)-y-CharSize,CharSize,CharSize)
        Col_X1=lengthCameraFrame+x
        Col_X2=lengthCameraFrame+x+CharSize
        Col_Y1=int(widthCameraFrame/2)-y-CharSize
        Col_Y2=int(widthCameraFrame/2)-y
    ObstacleX,EnemyPass=VirusCod(ObstacleX)
    #DrawFunction(screen,ObstacleX,ObstacleY,VirusWidthX,VirusWidthY)
    Col_XX=ObstacleX
    Col_YY=ObstacleY+VirusWidthY
    #DrawFunction(screen,lengthCameraFrame+x,int(widthCameraFrame/2)-y-CharSize,CharSize,CharSize)
    #Col_X,Col_Y,Col_XX,Col_YY=getCollisionPoint()
    if SanetizerLife>0:
        DrawFunction(screen,Col_X1,Col_Y1,Col_X2-Col_X1,Col_Y2-Col_Y1,[0,0,255])
        screen.blit(SanProt[SanetizerLife-1],(lengthCameraFrame,int(widthCameraFrame/2),widthCameraFrame,int(widthCameraFrame/2)))
    if DetectCollision(Col_X1,Col_Y1,Col_X2,Col_Y2,Col_XX,Col_YY,DangerOn)==1:
        if SanetizerLife>0:
            BoomVirus(screen,Col_Y1,Col_Y2,Col_XX,Col_YY-int(VirusWidthY/2),SanetizerLife)
            SanetizerLife-=1
            EnemyPass=1
            ObstacleX,y,jumpLim=reinitialize()
            flagJ=0
            Obstacle,ObstacleY,DangerOn,VType=GetObstacle()
        else:
            GameLives=GoExplosion(int(0.5*(Col_Y1+Col_Y2)),GameLives)
            EnemyPass=1
            ObstacleX,y,jumpLim=reinitialize()
            flagJ=0
            Obstacle,ObstacleY,DangerOn,VType=GetObstacle()
    elif DetectCollision(Col_X1,Col_Y1,Col_X2,Col_Y2,Col_XX,Col_YY,DangerOn)==2:
        SanetizerLife=3
        ObstacleX,y,jumpLim=reinitialize()
        Obstacle,ObstacleY,DangerOn,VType=GetObstacle()
    if GameLives<=0:
        GameOverScreen()
    if SkyLoop==1:
        SkyE,SkyY=SkyPropogate()
        SkyLoop=0
    SkyX,SkyLoop=SkyCod(SkyX)
    screen.blit(SkyE,(SkyX, SkyY))
    screen.blit(Obstacle,(ObstacleX, ObstacleY))
    pygame.display.update()
    if pygame.time.get_ticks()>=TimeofGame*1000:
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
