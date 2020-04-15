import pygame as pg
import random
from sprites import *
from settings import *
import time

class Game(object):
    def __init__(self):
        # Initialize window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.text_to_draw = "Flappy Bird"
        self.text_left_offset = WIDTH/2-105
        self.game_over = False
        self.high_score = 0 # Player high score

    def display_all_sprites(self):
        self.clock.tick(FPS)
        self.events() # Checking for pressing buttons, etc...
        self.update() # Updating all sprites and game
        self.draw() # Redrawing all sprites

    def new(self):
        # Start the Game
        self.all_sprites = pg.sprite.Group() # All sprites are here
        self.pipe_pair1 = PipePair(self, WIDTH+50) # Creating pipe pair 1
        self.pipe_pair2 = PipePair(self, WIDTH*1.7) # Creating pipe pair 2
        self.bird = Bird(self, self.pipe_pair1, self.pipe_pair2) # Creating the bird
        self.end = End_Screen(self)
        self.all_sprites.add(self.bird) # Adding bird to all sprites group
        self.all_sprites.add(self.pipe_pair1.bottom) # Adding bottom pipe from pipe pair 1 to all sprites group
        self.all_sprites.add(self.pipe_pair1.top) # Adding top pipe from pipe pair 1 to all sprites group
        self.all_sprites.add(self.pipe_pair2.bottom) # Adding bottom pipe from pipe pair 2 to all sprites group
        self.all_sprites.add(self.pipe_pair2.top) # Adding top pipe from pipe pair 2 to all sprites group

        self.clock.tick(FPS)
        self.update() # Updating all sprites
        self.draw() # Drawing all sprites

        for event in pg.event.get():
            if event.type == pg.KEYDOWN: # If SPACE is pressed
                if event.key == pg.K_SPACE:
                    self.bird.jump()
                    self.text_to_draw = str(self.bird.score)
                    self.text_left_offset = WIDTH/2-10
                    self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
                self.clock.tick(FPS)

                if self.game_over == False:
                    self.events() # Checking for pressing buttons, etc...
                    self.update() # Updating all sprites and game

                self.draw() # Redrawing all sprites

                if self.game_over:
                    self.events() # Checking for pressing buttons, etc...
                    self.end.update() # Updating, moving end screen with score and high score

    def update(self):
        # Updating the Game
        self.all_sprites.update()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT: # If X is pressed
                if self.playing: # Stopping game loop
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN: # If SPACE is pressed
                if event.key == pg.K_SPACE and self.game_over == False:
                    self.bird.jump() # Jump
                elif self.game_over: # If game is over
                    # Reseting settings
                    self.start_screen(self.text_to_draw, self.text_left_offset)
                    self.game_over = False
                    self.text_to_draw = str(self.bird.score)
                    self.text_left_offset = WIDTH/2-10
                    # Restarting the game
                    self.playing = False
                    self.text_to_draw = "Flappy Bird"
                    self.text_left_offset = WIDTH/2-105

    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        # Drawing all sprites
        self.all_sprites.draw(self.screen)
        self.start_screen(self.text_to_draw, self.text_left_offset)
        self.end.draw()

        pg.display.flip()

    def start_screen(self, text, position):
        msg = FONT_ARIAL.render(text, 0 , WHITE)
        self.screen.blit(msg, (position, HEIGHT/2-250))

g = Game()
while g.running:
    g.new()

pg.quit()
