"""Pong game environment module."""

import os
import sys

import pygame
import gymnasium as gym

from paddle import Paddle
from ball import Ball

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
        window_width: int = 1080,
        window_height: int = 720,
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

        # Initialize window size
        self.window_width = window_width
        self.window_height = window_height

        # Initialize render mode
        self.render_mode = render_mode

        # Initialize step repeat
        self.step_repeat = step_repeat

        # Enable headless mode when not using on-screen ('human') rendering so pygame can
        # run without a display (e.g., CI/servers). This must be set BEFORE calling
        # pygame.init() / pygame.display.set_mode() and only affects this process.
        if self.render_mode != 'human':
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            # Optional: also silence audio in headless environments.
            # os.environ['SDL_AUDIODRIVER'] = 'dummy'

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Pong")

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Initialize screen
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # Initialize fps
        self.fps = fps

        # Initialize background color (black)
        self.background_color = (0, 0, 0)

        # Initialize colors of players
        self.player_1_color = (102, 0, 204)  # Purple
        self.player_2_color = (255, 255, 204)  # Yellow

        # Initialize paddle dimensions
        self.paddle_height = 120
        self.paddle_width = 20

        # Initialize bot difficulty
        self.bot_difficulty = bot_difficulty

        # Initialize fonts
        self.font = pygame.font.SysFont(None, 70) 
        self.announcement_font = pygame.font.SysFont(None, 150)
        self.announcement_font.set_italic(True)

        # Initialize players
        self.player_1 = player_1
        self.player_2 = player_2

        # Initialize action space
        self.action_space = gym.spaces.Discrete(3)

        # Initialize AI agent
        self.ai_agent = ai_agent

        # Print initialization information
        print("Created a new PongGame instance, with the following parameters:")
        print("Player 1: ", self.player_1)
        print("Player 2: ", self.player_2)
        print("Render mode: ", self.render_mode)
        print("Step repeat: ", self.step_repeat)
        print("Bot difficulty: ", self.bot_difficulty)
        print("AI agent: ", self.ai_agent)

        # Initialize Game state
        self.reset()
     
    def reset(self) -> None:
        """Reset the game state.

        Initializes players' scores to zero and sets the top score target.
        """
        self.player_1_score = 0
        self.player_2_score = 0
        self.top_score = 20

        # Initialize player 1 paddle
        self.player_1_paddle = Paddle(
            x=50,
            y=self.window_height // 2 - self.paddle_height // 2,
            window_height=self.window_height,
            paddle_color=self.player_1_color,
        )
        # Initialize player 2 paddle
        self.player_2_paddle = Paddle(
            x=self.window_width - 50 - self.paddle_width,
            y=self.window_height // 2 - self.paddle_height // 2,
            window_height=self.window_height,
            paddle_color=self.player_2_color,
        )

        # Initialize ball
        self.ball = Ball(
            window_height=self.window_height,
            window_width=self.window_width,
            player_1_paddle=self.player_1_paddle,
            player_2_paddle=self.player_2_paddle,
        )

    def fill_background(self) -> None:
        """Clear the frame and draw static UI elements (e.g., scores)."""
        self.screen.fill(self.background_color)

        player_1_score_text = self.font.render(
            str(f'P1 Score: {self.player_1_score}'), True, self.player_1_color
        )
        player_2_score_text = self.font.render(
            str(f'P2 Score: {self.player_2_score}'), True, self.player_2_color
        )

        # Blit scores to screen
        self.screen.blit(player_1_score_text, (self.window_width // 4- 100, 10))
        self.screen.blit(player_2_score_text, (3 * self.window_width // 4 - 100, 10))
        
	
    def game_loop(self) -> None:
        """Run the interactive game loop until the window is closed."""
        # Main game loop; fill background and update display each frame.
        while True:
            # Clear frame background
            self.fill_background()
            player_1_action = 0
            player_2_action = 0

            # Handle events : when the user closes the window 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get keys pressed
            keys = pygame.key.get_pressed()

            # Player 1 actions if human player pressed w or s
            if self.player_1 == 'human':
                if keys[pygame.K_w]:
                    player_1_action = 1
                elif keys[pygame.K_s]:
                    player_1_action = 2
            
            # Player 2 actions if human player pressed up or down
            if self.player_2 == 'human':
                if keys[pygame.K_UP]:
                    player_2_action = 1
                elif keys[pygame.K_DOWN]:
                    player_2_action = 2
            
            # Print player actions
            if player_1_action != 0:
                print('Player 1 action: ', player_1_action)
            
            if player_2_action != 0:
                print('Player 2 action: ', player_2_action)

            # Step the environment
            self.step(
                player_1_action=player_1_action,
                player_2_action=player_2_action
            )

    def step(self, player_1_action: int, player_2_action: int) -> None:
        """Advance the environment by one frame and render if needed.

        Args:
            player_1_action: 0=none, 1=up, 2=down.
            player_2_action: 0=none, 1=up, 2=down.
        """
        player_1_reward = 0
        player_2_reward = 0
        done = False
        info = {}
        truncate = False


        player_1_reward = 0
        player_2_reward = 0
        info = {}
        done = False
        truncated = False

        for i in range(self.step_repeat):
            self._step(player_1_action=player_1_action,
                       player_2_action=player_2_action)

        ball_center = self.ball.x + (self.ball.width / 2)

        if(ball_center < 0):
            self.player_1_score += 1
            player_1_reward += 1
            player_2_reward -= 1
            self.ball.spawn()
        elif(ball_center > self.window_width):
            self.player_2_score += 1
            player_1_reward -= 1
            player_2_reward += 1
            self.ball.spawn()

        

    def _step(self, player_1_action: int, player_2_action: int) -> None:
        """Advance the environment by one frame and render if needed.

        Args:
            player_1_action: 0=none, 1=up, 2=down.
            player_2_action: 0=none, 1=up, 2=down.
        """


        # Move paddles
        self.player_1_paddle.move(player_1_action)
        self.player_2_paddle.move(player_2_action)

        # Fill background
        self.fill_background()

        # Draw paddles
        self.player_1_paddle.draw(self.screen)
        self.player_2_paddle.draw(self.screen)

        # Move ball
        self.ball.move()

        # Draw ball
        self.ball.draw(self.screen)


        # Render frame
        if self.render_mode == 'human':
            pygame.display.flip()
            if hasattr(self, 'clock'):
                self.clock.tick(self.fps)