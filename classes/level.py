from classes.car import *


class Level:

    def __init__(self):
        self.car = Car(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))

    def game_cycle(self):

        for event in pygame.event.get():

            if event == pygame.QUIT:
                quit()

        self.car.update()

    def draw(self, surface: pygame.Surface):
        self.surface.fill('grey')
        self.car.draw(self.surface)
        surface.blit(self.surface, (0, 0))
