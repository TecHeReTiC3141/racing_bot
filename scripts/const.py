import pygame
from pygame.locals import *
from math import *
from random import *
from pathlib import Path
import neat

pygame.init()

DISP_WIDTH = 1200
DISP_HEIGHT = 900


display = pygame.display.set_mode((10, 10))
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

MAX_GENS = 100