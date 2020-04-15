import pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
TITLE = "Flappy Bird"

# FPS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 153, 51)
YELLOW = (255, 255, 0)
ORANGE = (255, 214, 51)
WHITE = (255, 255, 255)
SILVER = (192,192,192)

# Player settings
PLAYER_GRAV = 0.8

# Pipes options
PIPE_SPEED = 2
DISTANCE_BITWEEN_PIPES = 160

# Fonts
FONT_ARIAL = pygame.font.SysFont("Arial", 50)
FONT_ARIAL_SMALL = pygame.font.SysFont("ARial", 35)
