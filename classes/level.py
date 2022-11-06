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
    size = 30

    def __init__(self, x, y):
        super().__init__(x, y, self.size, self.size)
        self.ridden_cars: dict[Car, bool] = {}
        self.surface.set_colorkey('yellow')
        self.surface.fill('yellow')
        pygame.draw.circle(self.surface, 'gold', (self.size // 2, self.size // 2), self.size // 2)

    def interact(self, car: Car):
        if self.ridden_cars.get(car, False):
            return
        if self.rect.colliderect(car.center_rect):
            car.g.fitness += self.value
            self.ridden_cars[car] = True


class BadMoney(Money):
    value = -200

    def __init__(self, x, y):
        super().__init__(x, y)
        self.surface.set_colorkey('yellow')
        self.surface.fill('yellow')
        pygame.draw.circle(self.surface, 'red', (self.size // 2, self.size // 2), self.size // 2)


class Finish(GameObject):
    value = 50

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.surface.fill('red')
        self.cars_loops: dict[Car, int] = {}

    def interact(self, car: Car, money: list[Money]):
        if car.delay <= 0 and self.rect.colliderect(car.rect):
            for mon in money:
                mon.ridden_cars[car] = False
            car.g.fitness += self.value
            car.delay = 200


class Level:

    def __init__(self, inner: list[tuple], outer: list[tuple],
                 coins: list[GameObject], finish_line: Finish, genome, config):
        self.genome = genome
        self.config = config
        self.cars: list[Car] = [Car(*finish_line.rect.center, g, config)
                     for _, g in genome]
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
        cars_alive = False
        for car in self.cars:
            if not car.alive:
                continue
            if self.mask.overlap(car.mask, car.surf_coords):
                car.alive = False
                car.g.fitness -= 50
                continue
            car.update(self.mask)

            # for obj in self.coins:
            #     obj.interact(car)
            # self.finish.interact(car, money=self.coins)
            cars_alive = True

        return cars_alive

    def draw(self, surface: pygame.Surface):
        self.surface.fill('grey')
        pygame.draw.polygon(self.surface, 'yellow', self.outer)
        pygame.draw.lines(self.surface, 'black', True, self.outer, width=2)
        self.finish.draw(self.surface)
        pygame.draw.polygon(self.surface, 'gray', self.inner)
        pygame.draw.lines(self.surface, 'black', True, self.inner, width=2)

        for car in self.cars:
            if not car.alive:
                continue
            car.draw(self.surface, self.show_dist)
            if self.switch_mask and self.mask.overlap(car.mask, car.surf_coords):
                overlap_mask = self.mask.overlap_mask(car.mask, car.surf_coords)
                overlap_mask = overlap_mask.to_surface()
                overlap_mask.set_colorkey('black')
                self.surface.blit(overlap_mask, (0, 0))
        for obj in self.coins:
            obj.draw(surface)

        self.surface.blit(font.render(f'Cars Remained: {len([i for i in self.cars if i.alive])}',
                                 True, 'red'), (300, 10))

        surface.blit(self.surface, (0, 0))
