import pygame
import sys
import json
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from sounds import *

def main():
    pygame.init()

    #pygame.mixer.init()
    #bg()
    #loop_bg()

    def load_high_score():
        try:
            with open("highscore.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
    
    

    def save_high_score(score):
        with open("highscore.json", "w") as file:
            json.dump(score, file)
    

    hight_score = load_high_score()

    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    font = pygame.font.Font(None, 50)
    current_score = 0
    score_increment = 1
    #hight_score = 0
    
    
    
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

        current_score_text = font.render(f"{current_score}", True, (54, 255, 142))
        screen.blit(current_score_text, (SCREEN_WIDTH // 2, 20))

        hight_score_text = font.render(f"High Score: {hight_score}", True, (54, 255, 142))
        screen.blit(hight_score_text, (20, 20))

        for obj in drawable:
            obj.draw(screen)
    
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collisionCheck(player):
                print("Game Over!")
                sys.exit()
            for shot in shots:
                if asteroid.collisionCheck(shot):
                    current_score += score_increment
                    asteroid.split()
                    shot.kill()

        if current_score > hight_score:
            hight_score = current_score
            save_high_score(hight_score)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        ms = clock.tick(60)
        dt = ms / 1000


if __name__ == "__main__":
    main()