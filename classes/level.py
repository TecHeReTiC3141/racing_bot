from classes.car import *


class Level:

    def __init__(self, inner: list[tuple], outer: list[tuple]):
        self.cars = [Car(DISP_WIDTH // 2, DISP_HEIGHT // 2)
                     for i in range(15)]
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.inner = inner
        self.outer = outer
        self.surface.set_colorkey('yellow')
        self.surface.fill('grey')
        pygame.draw.polygon(self.surface, 'yellow', self.outer)
        pygame.draw.polygon(self.surface, 'black', self.outer, width=2)

        pygame.draw.polygon(self.surface, 'gray', self.inner)
        pygame.draw.polygon(self.surface, 'black', self.inner, width=2)
        self.mask = pygame.mask.from_surface(self.surface)
        self.switch_mask = False
        self.show_dist = False
        self.show_lines_and_colls = True

    def game_cycle(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_m:
                    self.switch_mask = not self.switch_mask
                elif event.key == K_i:
                    self.show_dist = not self.show_dist
        for car in self.cars:
            car.update(self.mask)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('grey')
        pygame.draw.polygon(self.surface, 'yellow', self.outer)
        pygame.draw.lines(self.surface, 'black', True, self.outer, width=2)

        pygame.draw.polygon(self.surface, 'gray', self.inner)
        pygame.draw.lines(self.surface, 'black', True, self.inner, width=2)
        for car in self.cars:
            car.draw(self.surface, self.show_dist)
            if self.switch_mask and self.mask.overlap(car.mask, car.surf_coords):
                overlap_mask = self.mask.overlap_mask(car.mask, car.surf_coords)
                overlap_mask = overlap_mask.to_surface()
                overlap_mask.set_colorkey('black')
                self.surface.blit(overlap_mask, (0, 0))
        self.surface.blit(font.render(f"SHOW_DIST: {'YES' if self.show_dist else 'NO'}",
                                      True, 'red'), (10, 10))
        surface.blit(self.surface, (0, 0))
