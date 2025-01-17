from agents.openai_agent import OpenAIAgent
from games.simple_grid_game import SimpleGridGame




if __name__ == "__main__":
    game = SimpleGridGame(grid_size=10, tile_size=50)
    agent = OpenAIAgent(game_instance=game)
    game.run(agent)