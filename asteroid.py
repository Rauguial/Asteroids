import pygame
from circleshape import *
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (117,111,39), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt