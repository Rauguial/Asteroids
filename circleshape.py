import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass
    def update(self, dt):
        pass
    
    def collisionCheck(self, other, explosion_radius = None):
        #prev version
        """
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if distance <= self.radius + other.radius:
            return True
        return False
        """
        distance = pygame.math.Vector2.distance_to(self.position, other.position)

        if explosion_radius is None:
            return distance <= self.radius + other.radius
        
        else:
            return distance <= explosion_radius 