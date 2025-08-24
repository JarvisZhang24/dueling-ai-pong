from random import random
import numpy as np
import pygame

class Ball:
    """
    Ball class for the Pong game.

    Args:
        x: x-coordinate of the ball.
        y: y-coordinate of the ball.
        radius: radius of the ball.
        color: color of the ball.

    Returns:
        None
    """
    def __init__(self, 
                window_height: int,
                window_width: int,
                player_1_paddle: Paddle,
                player_2_paddle: Paddle,
                ball_color: tuple = (255, 255, 255),  # white
                ball_radius: int = 10
                ) -> None:

        # Initialize window height and width
        self.window_height = window_height
        self.window_width = window_width

        # Initialize paddles
        self.player_1_paddle = player_1_paddle
        self.player_2_paddle = player_2_paddle

        # Initialize ball color and radius
        self.ball_color = ball_color
        self.ball_radius = ball_radius

        # Initialize ball speed
        self.max_ball_speed = 30

        # Initialize last server
        self.last_server_left = random.choice([True, False])

        