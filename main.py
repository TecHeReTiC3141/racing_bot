from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Racing game')

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():

        if event == pygame.QUIT:
            quit()

    display.fill('gray')

    pygame.display.update()
    clock.tick(60)
