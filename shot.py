from constants import *
from circleshape import *


class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 34), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

class Bomb(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.timer = 5
        self.spawn_time = pygame.time.get_ticks()
        
    

    def draw(self, screen):
        pygame.draw.circle(screen, (209, 0, 0), self.position, self.radius)
        

   
        
            
    
    
