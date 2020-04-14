import pygame as pg
from settings import *
import random
import math
import time
vec = pg.math.Vector2

class Bird(pg.sprite.Sprite):
    def __init__(self, game, pipe_pair1, pipe_pair2):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2 - 100, HEIGHT / 2)
        self.pos = self.rect.center
        self.vel = vec(0, 0) # Moving
        self.acc = vec(0, 0) # Gravity
        self.score = 0
        self.pipe_pair1 = pipe_pair1
        self.pipe_pair2 = pipe_pair2

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.vel += self.acc
        self.pos += self.vel

        # Checking for collision with bottom wall
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT

        # Checking for a colission with pipes
        if (self.pos[0] > self.pipe_pair1.top.pos[0]-50 and self.pos[1] < self.pipe_pair1.top.pos[1]+20 and self.pos[0] < self.pipe_pair1.top.pos[0]+40):
            time.sleep(1)
            self.game.playing = False # Stopping game loop and restarting it
            # Reseting settings
            self.game.text_to_draw  ="Flappy Bird"
            self.score = 0
            self.game.text_left_offset = WIDTH/2-105
        elif (self.pos[0] > self.pipe_pair2.top.pos[0]-50 and self.pos[1] < self.pipe_pair2.top.pos[1]+20 and self.pos[0] < self.pipe_pair2.top.pos[0]+40):
            time.sleep(1)
            self.game.playing = False # Stopping game loop and restarting it
            # Reseting settings
            self.game.text_to_draw  ="Flappy Bird"
            self.score = 0
            self.game.text_left_offset = WIDTH/2-105
        elif self.pos[0] > self.pipe_pair1.bottom.pos[0]-50 and self.pos[1] > self.pipe_pair1.bottom.pos[1]-self.pipe_pair1.bottom.image.get_height() and self.pos[0] < self.pipe_pair1.bottom.pos[0]+40:
            time.sleep(1)
            self.game.playing = False # Stopping game loop and restarting it
            # Reseting settings
            self.game.text_to_draw  ="Flappy Bird"
            self.score = 0
            self.game.text_left_offset = WIDTH/2-105
        elif self.pos[0] > self.pipe_pair2.bottom.pos[0]-50 and self.pos[1] > self.pipe_pair2.bottom.pos[1]-self.pipe_pair2.bottom.image.get_height() and self.pos[0] < self.pipe_pair2.bottom.pos[0]+40:
            time.sleep(1)
            self.game.playing = False # Stopping game loop and restarting it
            # Reseting settings
            self.game.text_to_draw  ="Flappy Bird"
            self.score = 0
            self.game.text_left_offset = WIDTH/2-105
        # Checking for scoring
        elif (self.pos[0] > self.pipe_pair1.top.pos[0]-50 and self.pos[0] < self.pipe_pair1.top.pos[0]+50 and self.pos[1] > self.pipe_pair1.top.pos[1]) and (self.pos[1] < self.pipe_pair1.bottom.pos[1]-self.pipe_pair1.bottom.image.get_height()):
            self.score += self.pipe_pair1.value
            self.game.text_to_draw = str(self.score) # Updating score
            self.game.text_left_offset = WIDTH/2-10 # Moving Score to center of the screen
            self.pipe_pair1.value = 0
        elif (self.pos[0] > self.pipe_pair2.top.pos[0]-50 and self.pos[0] < self.pipe_pair2.top.pos[0]+50 and self.pos[1] > self.pipe_pair2.top.pos[1]) and (self.pos[1] < self.pipe_pair2.bottom.pos[1]-self.pipe_pair2.bottom.image.get_height()):
            self.score += self.pipe_pair2.value
            self.game.text_to_draw = str(self.score) # Updating score
            self.game.text_left_offset = WIDTH/2-10 # Moving Score to center of the screen
            self.pipe_pair2.value = 0


        self.rect.midbottom = self.pos # Setting the position

    def jump(self):
        self.vel.y = -10 # Jump

class PipePair(pg.sprite.Sprite):
    def __init__(self, game, x):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.bottom = PipeBottom(self.game, 80, random.randint(100, 400), x, self) # Creating pipe bottom

        #
        #Top pipe height must be:
        #
        #   Top_pipe_height = screen_height - bottom_pipe_heigth - DISTANCE_BITWEEN_PIPES
        #
        #|    | |                                |-|
        #|    |-| _                              | |
        #|         | <- distance bitween pipes   | |<--- Height of the screen
        #|     _  _|                             | |
        #|    | |                                | |
        #|____|_|________________________________|-|
        #     /\
        #     ||
        #     Bottom pipe
        #

        self.top = PipeTop(self.game, 80, HEIGHT-self.bottom.image.get_height(), x, self.bottom, self) # Creating pipe top
        self.value = 1

    def update(self):
        # Updating all pipes
        self.bottom.update()
        self.top.update()

class PipeTop(pg.sprite.Sprite):
    def __init__(self, game, width, height, x, bottom, pipe_pair):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.bottom = bottom
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.image.get_height()/2)# Setting position on top of the screen
        self.pos = self.rect.center
        self.pipe_pair = pipe_pair

    def update(self):
        self.pos += vec(-PIPE_SPEED, 0) # Moving the pipe

        # If pipe is off the screen
        if self.pos.x < -40:
            self.pipe_pair.value = 1
            self.pos.x = WIDTH+40
            self.image = pg.Surface((80, (HEIGHT-(self.bottom.image.get_height())/2-DISTANCE_BITWEEN_PIPES)*2))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.center = (self.pos.x, self.image.get_height()/2) # Setting position on top of the screen
            self.pos = self.rect.center

        self.rect.midbottom = self.pos # Setting the position

class PipeBottom(pg.sprite.Sprite):
    def __init__(self, game, width, height, x, pipe_pair):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, HEIGHT+(self.image.get_height()/2)) # Setting the position on bottom of the screen
        self.pos = self.rect.center
        self.pipe_pair = pipe_pair

    def update(self):
        self.pos += vec(-PIPE_SPEED, 0) # Moving the pipe

        # If pipe is off the screen
        if self.pos.x < -40:
            self.pipe_pair.value = 1
            self.pos.x = WIDTH+40
            self.image = pg.Surface((80, random.randint(100, 700))) # Setting random height
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.center = (self.pos.x, HEIGHT+(self.image.get_height()/2)) # Placing pipe in the bottom of the screen
            self.pos = self.rect.center

        self.rect.midbottom = self.pos # Setting the position
