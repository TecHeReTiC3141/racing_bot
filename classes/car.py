from scripts.const import *


class Car:
    SPEED_EPS = .15
    ANGLE_EPS = .05
    image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('images/bolid.png'), (25, 62)), 270).convert_alpha()

    def __init__(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 0
        self.angle = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface: pygame.Surface):
        rotated_image = pygame.transform.rotate(self.image, degrees(self.angle))
        # rotated_image.set_alpha(128)
        self.mask = pygame.mask.from_surface(rotated_image)
        # surface.blit(font.render(str(pygame.math.Vector2(round(cos(self.angle), 2), -round(sin(self.angle), 2))
        #                              * self.speed), True, 'black'), (10, 10))
        # surface.blit(self.mask.to_surface(), (self.rect.centerx - rotated_image.get_width() // 2,
        #                              self.rect.centery - rotated_image.get_height() // 2))

        surface.blit(rotated_image, (self.rect.centerx - rotated_image.get_width() // 2,
                                     self.rect.centery - rotated_image.get_height() // 2))
        # point of car 'echolocation'
        pygame.draw.circle(surface, 'green', (round(self.rect.centerx +
                                                    rotated_image.get_width() // 2 * cos(self.angle)),
                                              round(self.rect.centery -
                                                    rotated_image.get_height() // 2 * sin(self.angle))), 5)
        pygame.draw.circle(surface, 'green', (round(self.rect.centerx -
                                                    rotated_image.get_width() // 2 * cos(self.angle)),
                                              round(self.rect.centery +
                                                    rotated_image.get_height() // 2 * sin(self.angle))),
                           5)

        pygame.draw.circle(surface, 'red', (round(self.rect.centerx +
                                                    self.image.get_height() // 2 * sin(self.angle)),
                                              round(self.rect.centery +
                                                    self.image.get_height() // 2 * cos(self.angle))), 5)
        pygame.draw.circle(surface, 'red', (round(self.rect.centerx -
                                                    self.image.get_height() // 2 * sin(self.angle)),
                                              round(self.rect.centery -
                                                    self.image.get_height() // 2 * cos(self.angle))),
                           5)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.speed = min(self.speed + self.SPEED_EPS, 5)
        elif keys[K_s]:
            self.speed = max(self.speed - self.SPEED_EPS, -5)
        else:
            if self.speed > 0:
                self.speed -= self.SPEED_EPS / 2
            elif self.speed < 0:
                self.speed += self.SPEED_EPS / 2
        if keys[K_a]:
            self.angle += self.ANGLE_EPS
        if keys[K_d]:
            self.angle -= self.ANGLE_EPS

    def update(self):
        self.move()

        self.rect.move_ip(pygame.math.Vector2(cos(self.angle), -sin(self.angle)) * self.speed)
