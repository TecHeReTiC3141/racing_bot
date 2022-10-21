from scripts.const import *


class EchoPoint:

    def __init__(self, center: tuple, angle_delta, rotated: bool, dx_side: str, dy_side: str,
                 dx, dy, dx_func, dy_func, color='green', enabled=True):
        self.surface = pygame.Surface((10, 10))
        self.surface.set_colorkey('black')
        pygame.draw.circle(self.surface, 'green', (self.surface.get_width() // 2,
                                                   self.surface.get_height() // 2), 5)
        self.rect = self.surface.get_rect(center=center)
        self.angle_delta = angle_delta
        self.coll = self.rect.center
        self.dx_side = dx_side
        self.dy_side = dy_side

        self.dx = dx
        self.dy = dy

        self.dx_func = dx_func
        self.dy_func = dy_func

        self.color = color
        self.rotated = rotated
        self.enabled = enabled

    def update(self, center: pygame.Vector2, image_size, angle):
        width, height = image_size[0] // 2, image_size[1] // 2
        self.rect.centerx = round(center.x + (width if self.dx_side == 'width' else height)
                                  * self.dx * self.dx_func(angle))
        self.rect.centery = round(center.y + (width if self.dy_side == 'width' else height)
                                  * self.dy * self.dy_func(angle))

    def find_collisions(self, angle, mask: pygame.mask.Mask):
        cur_surf = pygame.Surface((1, 1))
        cur_point = pygame.Vector2(self.rect.center)
        cur_mask = pygame.mask.from_surface(cur_surf)
        angle += self.angle_delta
        angle %= (2 * pi)
        eps = .1
        while not mask.overlap(cur_mask, tuple(cur_point)) \
                and 0 <= cur_point.x <= DISP_WIDTH and 0 <= cur_point.y <= DISP_HEIGHT:

            if angle == pi / 2:
                bias = (0, -1 if angle < pi else 1)
            elif angle % pi == 0:
                bias = (-1 if angle == pi else 1, 0)
            elif 0 <= angle <= pi:
                bias = (eps if cos(angle) > 0 else -eps, -round(abs(tan(angle) * eps), 3))
            else:
                bias = (eps if cos(angle) > 0 else -eps, round(abs(tan(angle) * eps), 3))
            cur_point += bias
        self.coll = tuple(cur_point)

    @staticmethod
    def get_lines_intersection(x0, y0, angle) -> tuple:
        angle %= (2 * pi)
        if angle == pi / 2:
            return x0, 0 if angle < pi else DISP_HEIGHT
        if angle % pi == 0:
            return 0 if angle == pi else DISP_WIDTH, y0
        if 0 <= angle <= pi:
            return x0 + y0 / tan(angle), 0
        return x0 - (DISP_HEIGHT - y0) / tan(angle), DISP_HEIGHT

    def draw_coll_line(self, surface, angle, dist_angle, show_dist):
        dist_angle %= (2 * pi)
        angle = angle % (2 * pi) + self.angle_delta
        point, coll = pygame.Vector2(self.rect.center), pygame.Vector2(self.coll)
        pygame.draw.circle(surface, self.color, point, 5)
        pygame.draw.line(surface, 'darkgreen', point,
                         self.get_lines_intersection(*point, angle), 2)
        pygame.draw.circle(surface, 'red', coll, 5)
        if show_dist and dist(point, coll) > 60:
            dis = pygame.transform.rotate(small_font.render(str(round(dist(point, coll), 1)),
                                                            True, 'black'), round(degrees(dist_angle if dist_angle < pi
                                                                                          else dist_angle - pi)))
            dist_pos = point + (coll - point) / 2
            dist_pos.x -= dis.get_width() // 2
            dist_pos.y -= dis.get_height() // 2

            surface.blit(dis, dist_pos)


class RelEchoPoint(EchoPoint):

    def __init__(self, rel: EchoPoint, dx, dy):
        super().__init__(rel.rect.center, -rel.angle_delta, rel.rotated, 'width', 'height', dx, dy, sin, cos)
        self.rel = rel

    def update(self, center: pygame.Vector2, image_size, angle):
        self.rect.center = (self.rel.rect.centerx + cos(angle) * self.dx,
                            self.rel.rect.centery + sin(angle) * self.dy)


class Car:
    MAX_SPEED = 5.
    SPEED_EPS = .2
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

        self.echopoints: dict[str, EchoPoint] = {
            'forward': EchoPoint(self.rect.midright, 0, True, 'width', 'height', 1, -1, cos, sin),
            'back': EchoPoint(self.rect.midleft, pi, True, 'width', 'height', -1, 1, cos, sin),
            'left': EchoPoint(self.rect.midtop, -pi / 2, False, 'height', 'height', -1, -1, sin, cos, 'blue',
                              enabled=False),
            'right': EchoPoint(self.rect.midbottom, pi / 2, False, 'height', 'height', 1, 1, sin, cos,
                               enabled=False),
        }

        self.rel_echopoints: dict[str, RelEchoPoint] = {
            'forward_left': RelEchoPoint(self.echopoints['left'], self.rect.width // 10 * 3,
                                         -self.rect.width // 10 * 3),
            'forward_right': RelEchoPoint(self.echopoints['right'], self.rect.width // 10 * 3,
                                          -self.rect.width // 10 * 3),
            'back_left': RelEchoPoint(self.echopoints['left'], -self.rect.width // 10 * 3,
                                      self.rect.width // 10 * 4),
            'back_right': RelEchoPoint(self.echopoints['right'], -self.rect.width // 10 * 3,
                                       self.rect.width // 10 * 4),
        }

    def draw(self, surface: pygame.Surface, show_dist: bool):
        self.rotated_image = pygame.transform.rotate(self.image, round(degrees(self.angle)))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.surf_coords = self.rotated_image.get_rect(center=self.rect.center).topleft
        surface.blit(self.rotated_image, self.surf_coords)

        for echo in self.echopoints:
            if not self.echopoints[echo].enabled:
                continue
            self.echopoints[echo].draw_coll_line(surface, self.angle, 0, show_dist)

        for echo in self.rel_echopoints:
            if not self.rel_echopoints[echo].enabled:
                continue
            self.rel_echopoints[echo].draw_coll_line(surface, self.angle, 0, show_dist)

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

    def update(self, level_mask: pygame.mask.Mask):
        self.move()
        self.rect.move_ip((round(cos(self.angle) * self.speed),
                           round(-sin(self.angle) * self.speed)))

        for echo in self.echopoints:

            self.echopoints[echo].update(pygame.Vector2(self.rect.center),
                                         (self.rotated_image if self.echopoints[
                                             echo].rotated else self.image).get_size(),
                                         self.angle)
            self.echopoints[echo].find_collisions(self.angle, level_mask)

        for echo in self.rel_echopoints:
            self.rel_echopoints[echo].update(pygame.Vector2(self.rect.center),
                                             (self.rotated_image if self.rel_echopoints[
                                                 echo].rotated else self.image).get_size(),
                                             self.angle)
            self.rel_echopoints[echo].find_collisions(self.angle, level_mask)
