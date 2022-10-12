import pygame
from pygame.locals import *
from math import *
from random import *
from pathlib import Path

pygame.init()

DISP_WIDTH = 1000
DISP_HEIGHT = 800
MAP_WIDTH, MAX_HEIGHT = 128 * 20, 238 * 20
SCALE = DISP_WIDTH / MAP_WIDTH

display = pygame.display.set_mode((10, 10))
font = pygame.font.Font(None, 50)
