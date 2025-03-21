import pygame
import sys
from constants import *
from circleshape import *
from shot import *
from main import game_over_screen
#from main import *
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = PLAYER_HP
        self.bomb_cd = 0 #new

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw (self, screen):
        pygame.draw.polygon(screen, (255,255,255), self.triangle())
        

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self, position):
        
        if self.shoot_timer > 0:
            return

        self.shoot_timer = PLAYER_SHOOT_CD

        shot = Shot(position.x, position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    #new_try bombs
    def drop_bomb(self, position):
        if self.bomb_cd > 0:
            return
        
        self.bomb_cd = PLAYER_BOMB_CD
        bomb = Bomb(position.x, position.y, BOMB_RADIUS)

     
    def takeDamage(self, lives, damage):
        
        if self.lives > 0:
            self.lives -= damage
        #Dying is handled inside main.py
            

   

    def update(self, dt):
        self.bomb_cd -= dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot(self.position)
        #new
        if keys[pygame.K_LSHIFT]:
            self.drop_bomb(self.position)
   
    