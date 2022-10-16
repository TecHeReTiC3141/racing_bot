from scripts.const import *


class Car:
    SPEED_EPS = .15
    ANGLE_EPS = .05
    image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('images/bolid.png'),
                                                           (25, 62)), 270).convert_alpha()

    def __init__(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))
        self.rotated_image = self.image.copy()
        self.speed = 0
        self.angle = 0
        self.velocity = pygame.math.Vector2()
        self.acceleration = pygame.math.Vector2()
        self.surf_coords: tuple = self.rect.topleft
        self.mask = pygame.mask.from_surface(self.image)

        self.forward = self.rect.midright
        self.back = self.rect.midleft
        self.left = self.rect.midtop
        self.right = self.rect.midbottom

        self.forward_coll = self.rect.midright
        self.back_coll = self.rect.midleft
        self.left_coll = self.rect.midtop
        self.right_coll = self.rect.midbottom

    @staticmethod
    def get_lines_intersection(x0, y0, angle) -> tuple:
        angle %= (2 * pi)
        if angle == pi / 2:
            return x0, 0 if angle < pi else DISP_HEIGHT
        if angle % pi == 0:
            return  0 if angle == pi else DISP_WIDTH, y0
        if 0 <= angle <= pi:
            return x0 + y0 / tan(angle), 0
        return x0 - (DISP_HEIGHT - y0) / tan(angle), DISP_HEIGHT

    def draw(self, surface: pygame.Surface):
        self.rotated_image = pygame.transform.rotate(self.image, degrees(self.angle))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.surf_coords = self.rotated_image.get_rect(center=self.rect.center).topleft
        surface.blit(self.rotated_image, (self.surf_coords))
        # point of car 'echolocation'
        pygame.draw.circle(surface, 'green', self.forward, 5)
        pygame.draw.line(surface, 'darkgreen', self.forward,
                         self.get_lines_intersection(*self.forward, self.angle), 2)
        pygame.draw.circle(surface, 'green', self.back, 5)
        pygame.draw.line(surface, 'darkgreen', self.back, self.get_lines_intersection(*self.back, self.angle - pi))

        pygame.draw.circle(surface, 'yellow', self.left, 5)
        pygame.draw.line(surface, 'darkgreen', self.left, self.get_lines_intersection(*self.left, self.angle - pi / 2))
        pygame.draw.circle(surface, 'yellow', self.right, 5)
        pygame.draw.line(surface, 'darkgreen', self.right, self.get_lines_intersection(*self.right, self.angle + pi / 2))


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

    def update(self, level_mask: pygame.mask):
        self.move()
        self.rect.move_ip(pygame.math.Vector2(cos(self.angle), -sin(self.angle)) * self.speed)

        self.forward = (round(self.rect.centerx + self.rotated_image.get_width() // 2 * cos(self.angle)),
                        round(self.rect.centery - self.rotated_image.get_height() // 2 * sin(self.angle)))

        self.back = (round(self.rect.centerx - self.rotated_image.get_width() // 2 * cos(self.angle)),
                    round(self.rect.centery + self.rotated_image.get_height() // 2 * sin(self.angle)))

        self.left = (round(self.rect.centerx + self.image.get_height() // 2 * sin(self.angle)),
                      round(self.rect.centery + self.image.get_height() // 2 * cos(self.angle)))

        self.right = (round(self.rect.centerx - self.image.get_height() // 2 * sin(self.angle)),
                    round(self.rect.centery - self.image.get_height() // 2 * cos(self.angle)))
