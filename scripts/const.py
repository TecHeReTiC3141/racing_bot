import pygame
from pygame.locals import *
from math import *
from random import *
from pathlib import Path

pygame.init()

DISP_WIDTH = 1200
DISP_HEIGHT = 900
MAP_WIDTH, MAP_HEIGHT = 128 * 30, 128 * 20
XSCALE, YSCALE = DISP_WIDTH / MAP_WIDTH, DISP_HEIGHT / MAP_HEIGHT

display = pygame.display.set_mode((10, 10))
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
