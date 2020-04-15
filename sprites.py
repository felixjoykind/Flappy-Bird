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
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2 - 100, HEIGHT / 2)
        self.pos = self.rect.center
        self.vel = vec(0, 0) # Moving
        self.acc = vec(0, 0) # Gravity
        self.score = 0
        self.high_score = self.score
        self.pipe_pair1 = pipe_pair1
        self.pipe_pair2 = pipe_pair2

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.vel += self.acc
        self.pos += self.vel

        # Checking for collision with bottom wall
        if self.pos.y > HEIGHT:
            self.game.all_sprites.add(self.game.end)
            self.game.game_over = True # Means thet we should restart game
            # Reseting settings
            self.game.text_to_draw = "Game Over"
            self.game.text_left_offset = WIDTH/2-105

        # Checking for a colission with pipes
        if (self.pos[0] > self.pipe_pair1.top.pos[0]-55 and self.pos[1] < self.pipe_pair1.top.pos[1]+25 and self.pos[0] < self.pipe_pair1.top.pos[0]+40):
            self.game.all_sprites.add(self.game.end)
            self.game.game_over = True # Means thet we should restart game
            # Reseting settings
            self.game.text_to_draw = "Game Over"
            self.game.text_left_offset = WIDTH/2-105
        elif (self.pos[0] > self.pipe_pair2.top.pos[0]-55 and self.pos[1] < self.pipe_pair2.top.pos[1]+25 and self.pos[0] < self.pipe_pair2.top.pos[0]+40):
            self.game.all_sprites.add(self.game.end)
            self.game.game_over = True # Means thet we should restart game
            # Reseting settings
            self.game.text_to_draw = "Game Over"
            self.game.text_left_offset = WIDTH/2-105
        elif self.pos[0] > self.pipe_pair1.bottom.pos[0]-55 and self.pos[1] > self.pipe_pair1.bottom.pos[1]-self.pipe_pair1.bottom.image.get_height()+5 and self.pos[0] < self.pipe_pair1.bottom.pos[0]+40:
            self.game.all_sprites.add(self.game.end)
            self.game.game_over = True # Means thet we should restart game
            # Reseting settings
            self.game.text_to_draw = "Game Over"
            self.game.text_left_offset = WIDTH/2-105
        elif self.pos[0] > self.pipe_pair2.bottom.pos[0]-55 and self.pos[1] > self.pipe_pair2.bottom.pos[1]-self.pipe_pair2.bottom.image.get_height()+5 and self.pos[0] < self.pipe_pair2.bottom.pos[0]+40:
            self.game.all_sprites.add(self.game.end)
            self.game.game_over = True # Means thet we should restart game
            # Reseting settings
            self.game.text_to_draw = "Game Over"
            self.game.text_left_offset = WIDTH/2-105
        # Checking for scoring
        elif (self.pos[0] > self.pipe_pair1.top.pos[0]-50 and self.pos[0] < self.pipe_pair1.top.pos[0]+50 and self.pos[1] > self.pipe_pair1.top.pos[1]) and (self.pos[1] < self.pipe_pair1.bottom.pos[1]-self.pipe_pair1.bottom.image.get_height()):
            self.score += self.pipe_pair1.value
            if self.score > self.high_score:
                self.game.high_score = self.score
            self.game.text_to_draw = str(self.score) # Updating score
            self.game.text_left_offset = WIDTH/2-10 # Moving Score to center of the screen
            self.pipe_pair1.value = 0
        elif (self.pos[0] > self.pipe_pair2.top.pos[0]-50 and self.pos[0] < self.pipe_pair2.top.pos[0]+50 and self.pos[1] > self.pipe_pair2.top.pos[1]) and (self.pos[1] < self.pipe_pair2.bottom.pos[1]-self.pipe_pair2.bottom.image.get_height()):
            self.score += self.pipe_pair2.value
            if self.score > self.high_score:
                self.game.high_score = self.score
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

class End_Screen(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((200, 200))
        self.image.fill(SILVER)
        self.rect = self.image.get_rect()
        self.rect.center = (-160, 450)
        self.pos = self.rect.center
        self.game = game
    
    def update(self):
        self.pos += vec(10, 0) # Moving the board

        self.draw() # Drawing scores

        # Staying at current position
        if self.pos.x >= WIDTH/2:
            self.pos.x = WIDTH/2

        self.rect.midbottom = self.pos # Setting the position
    
    def draw(self):
        # Displaying current player score at the end of game
        msg = FONT_ARIAL_SMALL.render(f"Score: {self.game.bird.score}", 0 , WHITE)
        self.game.screen.blit(msg, (self.pos[0]-self.image.get_width()/4-5, self.pos[1]-self.image.get_height()+10))

        # Displaying player high score
        msg = FONT_ARIAL_SMALL.render(f"High Score: {self.game.high_score}", 0 , WHITE)
        self.game.screen.blit(msg, (self.pos[0]-self.image.get_width()/4-35, self.pos[1]-self.image.get_height()+60))
