from classes.car import *


class GameObject:
    value = 0

    def __init__(self, x, y, width, height):
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)


class Money(GameObject):
    value = 10

    def __init__(self, x, y):
        super().__init__(x, y, 70, 70)
        self.ridden_cars: dict[Car, bool] = {}
        self.surface.set_colorkey('yellow')
        self.surface.fill('yellow')
        pygame.draw.circle(self.surface, 'gold', (35, 35), 35)

    def interact(self, car: Car):
        if self.ridden_cars.get(car, False):
            return
        if self.rect.colliderect(car.rect):
            car.score += self.value
            self.ridden_cars[car] = True


class Finish(GameObject):
    value = 50

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.surface.fill('red')
        self.cars_loops: dict[Car, int] = {}

    def interact(self, car: Car, money: list[Money]):
        for mon in money:
            if not mon.ridden_cars.get(car, False):
                return
        if self.rect.colliderect(car.rect):
            for mon in money:
                mon.ridden_cars[car] = False
            car.score += self.value


class Level:

    def __init__(self, inner: list[tuple], outer: list[tuple],
                 coins: list[GameObject], finish_line: Finish):
        self.cars = [Car(DISP_WIDTH // 2, DISP_HEIGHT // 2)
                     for _ in range(1)]
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

        self.coins: list[Money] = coins
        self.finish = finish_line

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

            for obj in self.coins:
                obj.interact(car)
                self.finish.interact(car, money=self.coins)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('grey')
        pygame.draw.polygon(self.surface, 'yellow', self.outer)
        pygame.draw.lines(self.surface, 'black', True, self.outer, width=2)
        self.finish.draw(self.surface)
        pygame.draw.polygon(self.surface, 'gray', self.inner)
        pygame.draw.lines(self.surface, 'black', True, self.inner, width=2)

        for car in self.cars:
            car.draw(self.surface, self.show_dist)
            if self.switch_mask and self.mask.overlap(car.mask, car.surf_coords):
                overlap_mask = self.mask.overlap_mask(car.mask, car.surf_coords)
                overlap_mask = overlap_mask.to_surface()
                overlap_mask.set_colorkey('black')
                self.surface.blit(overlap_mask, (0, 0))
        for obj in self.coins:
            obj.draw(surface)

        self.surface.blit(font.render(f"SHOW_DIST: {'YES' if self.show_dist else 'NO'}",
                                      True, 'red'), (10, 10))
        self.surface.blit(font.render(f"CAR SCORE: {self.cars[0].score}",
                                      True, 'red'), (300, 10))
        surface.blit(self.surface, (0, 0))
