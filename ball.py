import pygame
import numpy as np
import random
from paddle import Paddle
class Ball:
    
    def __init__(self,
                 window_height,
                 window_width,
                 player_1_paddle: Paddle,
                 player_2_paddle: Paddle,
                 width=10,
                 height=10) -> None:
        self.height = height
        self.width = width
        self.window_height = window_height
        self.window_width = window_width
        self.player_1_paddle = player_1_paddle
        self.player_2_paddle = player_2_paddle
        self.ball_color = (255, 255, 255)
        self.max_speed = 30

        self.last_serve_left = random.choice([True, False])

        self.spawn()

    def spawn(self):
        self.x = self.window_width / 2
        self.y = self.window_height / 2

        speed = random.choice([10, 12, 14])

        # Flip X velocity every spawn
        self.last_serve_left = not self.last_serve_left
        self.vx = -speed if self.last_serve_left else speed

        self.vy = random.choice([-6, -4, -2, 2, 4, 6])

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def get_step_increment(self, vel):
        if(vel > 0):
            return 1
        else:
            return -1


    def draw(self, screen):
        pygame.draw.rect(screen, self.ball_color, (self.rect.x, self.rect.y, self.width, self.height))

    def move(self):
        new_x = self.x
        new_y = self.y
        x_step = self.get_step_increment(self.vx)
        y_step = self.get_step_increment(self.vy)
        new_rect = None
        
        early_collision_detected = False

        if(self.rect.colliderect(self.player_1_paddle) or 
               self.rect.colliderect((self.player_2_paddle))):
            early_collision_detected = True

        for i in range(abs(int(self.vy))):
            new_y = new_y + y_step

            if not early_collision_detected:
                if(not (0 <= new_y <= (self.window_height - self.height))):
                    self.vy = np.clip((self.vy * -1) + random.choice([-1, 1]), -self.max_speed, self.max_speed)
                    break

           
            new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

            if(new_rect.colliderect(self.player_1_paddle) or 
                   new_rect.colliderect(self.player_2_paddle)):
                self.vy = np.clip(self.vy + random.choice([-1, 1]), -self.max_speed, self.max_speed)
                break


        for i in range(abs(int(self.vx))):
            new_x = new_x + x_step

            if not early_collision_detected:
                new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                
                if(new_rect.colliderect(self.player_1_paddle) or 
                   new_rect.colliderect(self.player_2_paddle)):
                    # Invert the ball direction and speed up the ball slightly
                    self.vx = np.clip((self.vx + x_step) * -1, -self.max_speed, self.max_speed)
                    self.vy = np.clip(self.vy + random.choice([-1, 1]), -self.max_speed, self.max_speed)
                    break

        self.x = new_x
        self.y = new_y
        self.rect = pygame.Rect(new_x, new_y, self.width, self.height)