from classes.car import *


class Level:

    def __init__(self, inner: list[tuple], outer: list[tuple]):
        self.car = Car(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.inner = inner
        self.outer = outer



    def game_cycle(self):

        for event in pygame.event.get():

            if event == pygame.QUIT:
                quit()

        self.car.update()

    def draw(self, surface: pygame.Surface):
        self.surface.fill('grey')
        pygame.draw.polygon(self.surface, 'white', self.outer)
        pygame.draw.polygon(self.surface, 'black', self.outer, width=2)

        pygame.draw.polygon(self.surface, 'gray', self.inner)
        pygame.draw.polygon(self.surface, 'black', self.inner, width=2)
        self.car.draw(self.surface)
        surface.blit(self.surface, (0, 0))
