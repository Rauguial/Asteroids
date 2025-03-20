import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
import sys
def main():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    while True:
        screen.fill((0,0,0))

        for obj in drawable:
            obj.draw(screen)
    
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collisionCheck(player):
                print("Game Over!")
                sys.exit()
            for shot in shots:
                if asteroid.collisionCheck(shot):
                    asteroid.split()
                    shot.kill()



        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        ms = clock.tick(60)
        dt = ms / 1000


if __name__ == "__main__":
    main()