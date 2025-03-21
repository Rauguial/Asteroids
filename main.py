import pygame
import sys
import json
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from sounds import *



#Initialize pygame
pygame.init()

#Setting screen size and background image
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("assets/trythisbg.jpg")

#Set font 
font = pygame.font.Font(None, 50)
    
#Highscore loading
def load_high_score():
    try:
        with open("highscore.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
#Highscore saving
def save_high_score(score):
    with open("highscore.json", "w") as file:
        json.dump(score, file)



#Play again visuals
def draw_play_again_button():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)
    pygame.draw.rect(screen,(255, 255, 255), button_rect)
    font_small = pygame.font.Font(None, 24)
    text = font_small.render("Play Again", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

#Game Over Screen and Functions
def game_over_screen():
    screen.fill((0, 0, 0))
    text = font.render("Game Over! Press Enter to play again", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    screen.blit(text, text_rect)

    play_again_button_rect = draw_play_again_button()
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and play_again_button_rect.collidepoint(event.pos):
                    return

           
def main():
    
    while True: #Keep restarting when game over

        #Load high score
        hight_score = load_high_score()

        #Reset dynamic game state
        clock = pygame.time.Clock()
        dt = 0
        current_score = 0
        score_increment = 1

        #Setting up sprite.Groups
        asteroids = pygame.sprite.Group()
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        #Setting up containers
        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        Shot.containers = (shots, updatable, drawable)

        #Defining asteroidfield and player + placing player in the middle of the screen
        asteroidfield = AsteroidField()
        
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.lives = PLAYER_HP

        running = True
        while running:
            #Fill screen
            screen.fill((0,0,0))
            #add background after screen fill to show bg on top
            screen.blit(bg, (0, 0))

            #Display score
            current_score_text = font.render(f"{current_score}", True, (54, 255, 142))
            screen.blit(current_score_text, (SCREEN_WIDTH // 2, 20))
            #Display highscore
            hight_score_text = font.render(f"High Score: {hight_score}", True, (54, 255, 142))
            screen.blit(hight_score_text, (20, 20))

            #Draw all objects in the drawable Group separately on screen
            for obj in drawable:
                obj.draw(screen)
        
            #Update all objects in updatable Group
            updatable.update(dt)


            #Check individual asteroids for collision with player, with shots
            for asteroid in asteroids:
                if asteroid.collisionCheck(player):
                    player.takeDamage(player, 1)
                    print(player.lives)
                    asteroid.kill()

                    if player.lives <= 0:
                        running = False  #End game loop

                for shot in shots:
                    if asteroid.collisionCheck(shot):
                        current_score += score_increment #Add to score for each time an asteroid is shot
                        asteroid.split()
                        shot.kill()

            #Update highscore, and save it, if current score is higher than current highscore 
            if current_score > hight_score:
                hight_score = current_score
                save_high_score(hight_score)


            #Show the game
            pygame.display.flip()

            #Make closing the game work without crash message
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
            #Delta time
            ms = clock.tick(60)
            dt = ms / 1000
        
        #Show Game Over Screen and wait for restart
        game_over_screen()


if __name__ == "__main__":
    main()