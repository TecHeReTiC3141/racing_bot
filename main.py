from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Racing game')

clock = pygame.time.Clock()
level = Level()

while True:

    level.draw(display)
    level.game_cycle()

    pygame.display.update()
    clock.tick(60)
