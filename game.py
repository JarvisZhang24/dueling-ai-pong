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
        window_width: int = 720,
        window_height: int = 480,
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
        # run without a display (e.g., CI or servers). This must be set BEFORE calling
        # pygame.init() / pygame.display.set_mode() and only affects this process.
        if (self.render_mode != 'human'):
          os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Pong")

        # Initialize clock
        pygame.clock = pygame.time.Clock()

        # Initialize screen
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # Initialize fps
        self.fps = fps

        # Initialize colors of players
        self.player_1_color = (102 , 0 , 204) # Purple
        self.player_2_color = (255 , 255 , 204) # Yellow

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
     
    '''
    Reset the game state
    '''
    def reset(self):
          pass
	
    '''
    Game loop
    '''
    def game_loop(self):

        while(True):

            player_1_action = 0
            player_2_action = 0

            # Handle events : when the user closes the window 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get keys pressed
            keys = pygame.key.get_pressed()

            # Player 1 actions
            if self.player_1 == 'human':
                if keys[pygame.K_w]:
                    player_1_action = 1
                elif keys[pygame.K_s]:
                    player_1_action = 2
            
            # Player 2 actions
            if self.player_2 == 'human':
                if keys[pygame.K_UP]:
                    player_2_action = 1
                elif keys[pygame.K_DOWN]:
                    player_2_action = 2
            
            print('Player 1 action: ', player_1_action)
            print('Player 2 action: ', player_2_action)
                



            
            
		
		

         
         


        




        

     

            
        


