from scripts.const import *

class Car:
    image = pygame.image.load('images/bolid.png').convert_alpha()

    def __init__(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

    def draw(self, surface: pygame.Surface):
        rotated_image = pygame.transform.rotate(self.image, degrees(self.angle))