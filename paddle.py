from random import random
import numpy as np
import pygame

class Paddle:
    """
    Paddle class for the Pong game.

    Args:
        x: x-coordinate of the paddle.
        y: y-coordinate of the paddle.
        width: width of the paddle.
        height: height of the paddle.
        color: color of the paddle.

    Returns:
        None

    """
    def __init__(self, 
                 x: int,
                 y: int,
                 window_height: int,
                 width: int = 20,
                 height: int = 120,
                 paddle_color: tuple = (255, 255, 255) # white
                 ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Initialize paddle color
        self.paddle_color = paddle_color

        # Initialize paddle rectangle
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Initialize paddle speed
        self.speed = 15

        # Initialize window height
        self.window_height = window_height



    def draw(self, screen: pygame.Surface) -> None:

        # Draw paddle
        pygame.draw.rect(screen, self.paddle_color, (self.x, self.y, self.width, self.height))

    def move(self, direction: int) -> None:
        # Make sure direction is valid
        assert direction in [0, 1, 2]

        if direction == 0:
            return
        elif direction == 1:
            new_y = self.y - self.speed
        elif direction == 2:
            new_y = self.y + self.speed

        # Check if new_y is within bounds
        if 0 <= new_y <= self.window_height - self.height:
            self.y = new_y
        
        # Update paddle rectangle
        self.rect.topleft = (self.x, self.y)

    
