from agents.agents import LLMAgent
from games.simple_grid_game import SimpleGridGame




if __name__ == "__main__":
    game = SimpleGridGame(grid_size=10, tile_size=50)
    agent = LLMAgent(game_instance=game)
    game.run(agent)