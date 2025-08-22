"""Pong game environment module."""

import pygame
import sys
import numpy as np
import gymnasium as gym
import os

class PongGame(gym.Env):
    """Pong game environment built on Gymnasium.

    Attributes:
        window_width: Window width in pixels.
        window_height: Window height in pixels.
        fps: Target frames per second.
        player_1: Player 1 controller ('ai', 'bot', 'human').
        player_2: Player 2 controller ('ai', 'bot', 'human').
        render_mode: 'rgb_array' or 'human'.
        step_repeat: Number of frames to repeat each action.
        bot_difficulty: 'easy', 'medium', or 'hard'.
        ai_agent: Optional external agent/controller.
    """

    def __init__(
        self,
        window_width: int = 1280,
        window_height: int = 960,
        fps: int = 60,
        player_1: str = 'ai',
        player_2: str = 'bot',
        render_mode: str = 'rgb_array',
        step_repeat: int = 4,
        bot_difficulty: str = 'hard',
        ai_agent=None,
    ) -> None:
        """Initialize the Pong environment.

        Args:
            window_width: Window width in pixels.
            window_height: Window height in pixels.
            fps: Target frames per second.
            player_1: Controller for player 1 ('ai', 'bot', 'human').
            player_2: Controller for player 2 ('ai', 'bot', 'human').
            render_mode: 'rgb_array' for offscreen or 'human' for on-screen.
            step_repeat: Number of frames to repeat an action.
            bot_difficulty: Difficulty level for built-in bot ('easy'/'medium'/'hard').
            ai_agent: External agent instance when using AI control.

        Raises:
            ValueError: If an invalid player type is provided.
        """
        super().__init__()

        for p in [player_1, player_2]:
            if p not in ['ai', 'bot', 'human']:
                raise ValueError(f"Player {p} is not a valid player type.")

        self.window_width = window_width
        self.window_height = window_height
        self.render_mode = render_mode
        self.step_repeat = step_repeat

        # Enable headless mode when not using on-screen ('human') rendering so pygame can
        # run without a display (e.g., CI or servers). This must be set BEFORE calling
        # pygame.init() / pygame.display.set_mode() and only affects this process.
        if (self.render_mode != 'human'):
          os.environ['SDL_VIDEODRIVER'] = 'dummy'

        pygame.init()
        pygame.display.set_caption("Pong")

        self.clock = pygame.time.Clock()
        

     

            
        


