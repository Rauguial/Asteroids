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
    bg = pygame.image.load("assets/trythisbg.jpg")

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
    

    def draw_play_again_button(screen):
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)
        pygame.draw.rect(screen,(255, 255, 255), button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Play Again", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        return button_rect


    #Game Over Screen and Functions
    def gameOver(screen, clock):
        font = pygame.font.Font(None, 80)
        text = font.render("Game Over! Press Enter to play again", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(text, text_rect)

        play_again_button_rect = draw_play_again_button(screen)
        pygame.display.flip()
    
        while True:
            for event in pygame.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #left mouse button
                        if play_again_button_rect.collidepoint(event.pos):
                            main()
                    


    while True:
        screen.fill((0,0,0))
        #add background after screenfill to show bg on top
        screen.blit(bg, (0, 0))


        current_score_text = font.render(f"{current_score}", True, (54, 255, 142))
        screen.blit(current_score_text, (SCREEN_WIDTH // 2, 20))

        hight_score_text = font.render(f"High Score: {hight_score}", True, (54, 255, 142))
        screen.blit(hight_score_text, (20, 20))

        for obj in drawable:
            obj.draw(screen)
    
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collisionCheck(player):
                player.takeDamage(player, 1)
                print(player.lives)
                asteroid.kill()

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