
import pygame
from pygame.locals import *
from random import randint, choice
import time

size = (700,500)


class BackgroundColor:
    def __init__(self):
        self.color = (randint (0,200),randint (0,200), randint (0,200))
    def newRandomColor(self):
        self.color = (randint (0,200),randint (0,200), randint (0,200))
    
class Ball:
    def __init__(self,radius,color,xcor,ycor,xvel,yvel):
        self.radius = radius
        self.color = color
        self.xcor = xcor
        self.ycor = ycor
        self.xvel = xvel
        self.yvel = yvel
        self.rect = pygame.Rect(self.xcor,self.ycor,2*self.radius,2*self.radius)

    def move (self,paddle):
        if self.ycor < 0 or self.ycor > 500 - 2*self.radius:
            self.yvel = -self.yvel
        if self.xcor < 0 or self.xcor > 700 - 2*self.radius:
            self.xvel = -self.xvel
        if self.rect.colliderect(paddle):
            self.xvel = - self.xvel
        self.xcor += self.xvel
        self.ycor += self.yvel
        self.rect = pygame.draw.rect(screen,self.color,
                                     [self.xcor,self.ycor,2*self.radius,2*self.radius])
    
class Paddle:
    def __init__(self,xcor,ycor,height,width,color):
        self.xcor = xcor
        self.ycor = ycor
        self.height = height
        self.width = width
        self.color = color
        self.move = 0 #so that the paddle won't move at first
        self.rect = pygame.Rect(self.xcor, self.ycor,self.width,self.height)

    def draw(self):
        self.ycor += self.move
        #Dont go off to the bottom of the screen algorigthm
        if self.ycor > 500 - self.height: #if the ycor is off the bottom of the screen
            self.ycor = 500 - self.height #reset the ycor to the bottom
            self.move = 0 #stop moving
        #don't go off to the top of the screen either algorithm
        if self.ycor < 0: # if the ycor is off the screen
            self.ycor = 0 # reset the ycor to the top
            self.move = 0 #stop moving
        self.rect = pygame.draw.rect(screen,self.color,
                                     [self.xcor,self.ycor,self.width,self.height])
class Score:
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.score = 0
    
    def increaseScore(self,value):
        #print "gets to increaseScore"
        self.score += value

    def displayScore(self):
        # This is a font we use to draw text on the screen (size 72)
        font = pygame.font.SysFont("couriernew", 72)
        text =  font.render(str(self.score), True, GREEN)
        screen.blit(text, [self.xpos, self.ypos])
        
    def resetScore(self):
        self.score = 0

def drawNet ():
        '''draws the net down the screen's middle so that the user knows where the halfway point is'''
        y = 0 #start at top of the screen
        while y < 500: # keep goint until you reach the bottom
            pygame.draw.rect(screen,GREEN,[350,y,10,10]) #draw a square
            y += 20 # next y- value

#define the colors/ the constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,150,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
VIOLET = (238, 130,238, 1)
RANDOM = (randint(0,200),randint(0,200),randint(0,200))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size)

#Loop until the user clicks the close button.
done = False

#Used to manage how fast the screen updates
clock = pygame.time.Clock()

#create the ball which is actually a square, just like the original pong game
ball = Ball(5, #radius parameter
            WHITE, #color parameter
            randint(0,650), #x- value NOTE TO SELF IMPORTANT @#$%^&*! make ball spawn random in Breakout.io in javascript of Khel.io
            randint(0,450), #y- value
            1, #x- velocity
            2) #y- velocity

global bgc
bgc = BackgroundColor()


#create the paddles:
leftpaddle = Paddle(50,#xcor
                    randint(50,450),#ycor
                    50,#height
                    10,#width
                    BLUE) #color

rightpaddle = Paddle(650,#xcor
                    randint(50,450),#ycor
                    50,#height
                    10,#width
                    RED) #color



leftscore = Score(270,25)
rightscore = Score(400,25)

s = pygame.mixer.Sound("ledodis.wav")

while not done:
    for event in pygame.event.get(): #Check all the clicks and keystrokes
        if event.type == pygame.QUIT: #If the user clicked X to close this window
            done == True #stop repeating this loop and close the program
        if event.type == pygame.KEYDOWN: #if a key is pressed
            if event.key == K_UP: #if the up arrow key is pressed
                rightpaddle.move = -5 #The right paddle will go up
            if event.key == K_DOWN: #if the down arrow key is pressed
                rightpaddle.move = 5 #The right paddle should go down
            if event.key == K_w: #if the W key is pressed
                leftpaddle.move = -5 #the leftpaddle will move up
            if event.key == K_s: #if the S key is pressed
                leftpaddle.move = 5 #the leftpaddle will move down
        if event.type == pygame.KEYUP: #if a key is released
            if event.key == K_UP or event.key == K_DOWN: # if it's the up or down key
                rightpaddle.move = 0 #stop the right paddle
            if event.key == K_w or event.key == K_s: # if it's the w or s key
                leftpaddle.move = 0 # stop the left paddle
    
    screen.fill(bgc.color)
    
    if ball.xcor - (2 * ball.radius) <= 0:
        #print "left side hit"
        bgc.newRandomColor()
        rightscore.increaseScore(1)
        s.play()
        ball.xcor = 350
        
    if ball.xcor + (2 * ball.radius) >= 700:
        #print "right side hit"
        bgc.newRandomColor()
        leftscore.increaseScore(1)
        s.play()
        ball.xcor = 350
    #draw the net
    drawNet()

    #move the ball
    for paddle in [leftpaddle, rightpaddle]:
        ball.move(paddle)

        #move the paddles
    leftpaddle.draw()
    rightpaddle.draw()

    #display the score
    leftscore.displayScore()
    rightscore.displayScore()

    if leftscore.score == 5 or rightscore.score == 5:
        waiting = True
        while waiting:
            font = pygame.font.Font(None, 36)
            text = font.render("GAME OVER. PLAY AGAIN? Y/N", True, GREEN)
            screen.blit(text, [200,250])
            for event in pygame.event.get():
                if event.type  == pygame.KEYDOWN:
                    if event.key == K_y:
                        leftscore.resetScore()
                        rightscore.resetScore()
                        waiting = False
                        break
                    if event.key == K_n:
                        waiting = False
                        done = True
                        break
            pygame.display.update()
                

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
