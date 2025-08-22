from game import PongGame

env = PongGame(render_mode='human', 
               player_1='human', 
               player_2='human',
               bot_difficulty='easy')

env.game_loop()


