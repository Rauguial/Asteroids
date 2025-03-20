import pygame
import random
from circleshape import *
from constants import *
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255,162,0), self.position, self.radius)

        
    def split(self):
        
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        new_vec1 = self.velocity.rotate(random_angle)
        new_vec2 = self.velocity.rotate(-random_angle)
        new_rad = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_rad)
        asteroid_1.velocity = new_vec1 * 1.2

        asteroid_2 = Asteroid(self.position.x, self.position.y, new_rad)
        asteroid_2.velocity = new_vec2 * 1.2

    def update(self, dt):
        self.position += self.velocity * dt
    
    
            