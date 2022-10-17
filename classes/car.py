from scripts.const import *


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
            return 0 if angle == pi else DISP_WIDTH, y0
        if 0 <= angle <= pi:
            return x0 + y0 / tan(angle), 0
        return x0 - (DISP_HEIGHT - y0) / tan(angle), DISP_HEIGHT

    @staticmethod
    def get_mask_coll(point: tuple, angle, mask: pygame.mask.Mask) -> tuple:
        cur_surf = pygame.Surface((1, 1))
        cur_point = pygame.Vector2(point)
        cur_mask = pygame.mask.from_surface(cur_surf)
        angle %= 2 * pi
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
        return tuple(cur_point)

    def draw_coll_line(self, surface, point: tuple, angle, coll, dist_angle, show_dist):
        dist_angle %= (2 * pi)
        point, coll = pygame.Vector2(point), pygame.Vector2(coll)
        pygame.draw.circle(surface, 'green', point, 5)
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

    def draw(self, surface: pygame.Surface, show_dist: bool):
        self.rotated_image = pygame.transform.rotate(self.image, round(degrees(self.angle)))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.surf_coords = self.rotated_image.get_rect(center=self.rect.center).topleft
        surface.blit(self.rotated_image, self.surf_coords)

        # points of car 'echolocation'
        self.draw_coll_line(surface, self.forward, self.angle,
                            self.forward_coll, self.angle, show_dist)
        self.draw_coll_line(surface, self.back, self.angle - pi,
                            self.back_coll, self.angle, show_dist)
        self.draw_coll_line(surface, self.left, self.angle + pi / 2,
                            self.left_coll, self.angle - pi / 2, show_dist)
        self.draw_coll_line(surface, self.right, self.angle - pi / 2,
                            self.right_coll, self.angle - pi / 2, show_dist)

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

        self.forward = (round(self.rect.centerx + self.rotated_image.get_width() // 2 * cos(self.angle)),
                        round(self.rect.centery - self.rotated_image.get_height() // 2 * sin(self.angle)))

        self.forward_coll = self.get_mask_coll(self.forward, self.angle, level_mask)

        self.back = (round(self.rect.centerx - self.rotated_image.get_width() // 2 * cos(self.angle)),
                     round(self.rect.centery + self.rotated_image.get_height() // 2 * sin(self.angle)))

        self.back_coll = self.get_mask_coll(self.back, self.angle - pi, level_mask)

        self.left = (round(self.rect.centerx + self.image.get_height() // 2 * sin(self.angle)),
                     round(self.rect.centery + self.image.get_height() // 2 * cos(self.angle)))

        self.left_coll = self.get_mask_coll(self.left, self.angle + pi / 2, level_mask)

        self.right = (round(self.rect.centerx - self.image.get_height() // 2 * sin(self.angle)),
                      round(self.rect.centery - self.image.get_height() // 2 * cos(self.angle)))

        self.right_coll = self.get_mask_coll(self.right, self.angle - pi / 2, level_mask)
