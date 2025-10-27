import pygame
import random
import os

# COLORS RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# TILE TYPES
EMPTY = 0
WALL = 1
START = 2
GOAL = 3


class SimpleGridGame:
    def __init__(self, grid_size=10, tile_size=50):
        pygame.init()
        
        self.grid_size = grid_size    # e.g. 10 means 10×10
        self.tile_size = tile_size    # Each grid cell will be 50px by default
        
        # Window dimensions
        self.width = self.grid_size * self.tile_size
        self.height = self.grid_size * self.tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Grid Game")

        # Colors (R, G, B)
        self.color_empty = (255, 255, 255)  # white
        self.color_wall  = (0, 0, 0)        # black
        self.color_start = (255, 0, 0)      # red
        self.color_goal  = (0, 255, 0)      # green
        self.color_player= (0, 0, 255)      # blue

        # Create a 2D map array to hold cell types:
        self.map_data = [[EMPTY for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Define start (S) and goal (G) positions
        self.start_pos = (0, 0)  # top-left
        self.goal_pos  = (self.grid_size - 1, self.grid_size - 1)  # bottom-right

        # Mark them in the map
        start_x, start_y = self.start_pos
        goal_x, goal_y = self.goal_pos
        self.map_data[start_y][start_x] = START
        self.map_data[goal_y][goal_x] = GOAL

        # Current player position (starts at S)
        self.player_x, self.player_y = start_x, start_y

        # Generate some random walls
        self.generate_walls()

        # Track the number of steps
        self.num_steps = 0
        self.move_history = []

        # Font for rendering text
        self.font = pygame.font.SysFont(None, 32)

        # Whether the player has reached the goal
        self.reached_goal = False

    
    def get_events(self):
        return pygame.event.get()
    

    def generate_walls(self):
        """Randomly generate 0-4 walls of small random sizes in the grid."""
        # TODO: make sure that it is possible to reach the goal.
        wall_count = random.randint(0, 4)
        for _ in range(wall_count):
            # Random top-left corner for the wall
            wall_x = random.randint(0, self.grid_size - 1)
            wall_y = random.randint(0, self.grid_size - 1)
            # Random dimensions for the wall (width, height)
            wall_width = random.randint(1, 3)
            wall_height = random.randint(1, 3)

            for row in range(wall_y, min(wall_y + wall_height, self.grid_size)):
                for col in range(wall_x, min(wall_x + wall_width, self.grid_size)):
                    # Ensure we don't overwrite start or goal
                    if (col, row) != self.start_pos and (col, row) != self.goal_pos:
                        self.map_data[row][col] = WALL  # mark wall

    def move_up(self):
        """Try moving the player up one cell (same as pressing UP arrow)."""
        new_y = self.player_y - 1
        self.num_steps += 1
        self.move_history.append("move_up")
        if self.can_move_to(self.player_x, new_y):
            self.player_y = new_y
            self.check_goal_reached()

    def move_down(self):
        """Try moving the player down one cell (same as pressing DOWN arrow)."""
        new_y = self.player_y + 1
        self.num_steps += 1
        self.move_history.append("move_down")
        if self.can_move_to(self.player_x, new_y):
            self.player_y = new_y
            self.check_goal_reached()

    def move_left(self):
        """Try moving the player left one cell (same as pressing LEFT arrow)."""
        new_x = self.player_x - 1
        self.num_steps += 1
        self.move_history.append("move_left")
        if self.can_move_to(new_x, self.player_y):
            self.player_x = new_x
            self.check_goal_reached()

    def move_right(self):
        """Try moving the player right one cell (same as pressing RIGHT arrow)."""
        new_x = self.player_x + 1
        self.num_steps += 1
        self.move_history.append("move_right")
        if self.can_move_to(new_x, self.player_y):
            self.player_x = new_x
            self.check_goal_reached()

    def can_move_to(self, x, y):
        """Check if the player can move to cell (x, y)."""
        # Check boundaries
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return False
        if self.map_data[y][x] == WALL:
            return False
        return True

    def check_goal_reached(self):
        """Check if the player has reached the goal."""
        if (self.player_x, self.player_y) == self.goal_pos:
            self.reached_goal = True

    def draw_grid(self, surface):
        """Draw the grid cells on the given surface."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_value = self.map_data[row][col]
                rect = pygame.Rect(col * self.tile_size, 
                                   row * self.tile_size, 
                                   self.tile_size, self.tile_size)
                if cell_value == WALL:
                    color = self.color_wall
                elif cell_value == START:
                    color = self.color_start
                elif cell_value == GOAL:
                    color = self.color_goal
                else:
                    color = self.color_empty

                pygame.draw.rect(surface, color, rect)

        # Draw the player as a blue square
        player_rect = pygame.Rect(self.player_x * self.tile_size,
                                  self.player_y * self.tile_size,
                                  self.tile_size, self.tile_size)
        pygame.draw.rect(surface, self.color_player, player_rect)

        # (Optional) Draw grid lines to visualize cells
        for i in range(self.grid_size + 1):
            # vertical line
            pygame.draw.line(surface, (200, 200, 200), 
                             (i * self.tile_size, 0), 
                             (i * self.tile_size, self.height))
            # horizontal line
            pygame.draw.line(surface, (200, 200, 200), 
                             (0, i * self.tile_size), 
                             (self.width, i * self.tile_size))

    def show_end_message(self):
        """Show a message indicating the number of steps used."""
        text = f"You reached the goal in {self.num_steps} steps!"
        text_surface = self.font.render(text, True, (255, 255, 255))
        
        # Draw a black rectangle as a background for the text
        rect_width = text_surface.get_width() + 20
        rect_height = text_surface.get_height() + 20
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2
        
        pygame.draw.rect(self.screen, (0, 0, 0), 
                         (rect_x, rect_y, rect_width, rect_height))
        self.screen.blit(text_surface, (rect_x + 10, rect_y + 10))


    def run(self, agent):
        clock = pygame.time.Clock()
        step_count = 0
        while True:
            clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            if not self.reached_goal:
                # ascii_world = game.get_ascii_game_world()
                image_world = self.get_image_game_world(step_count)

                agent.step(world=image_world, steps_taken=step_count)

                step_count += 1

            # Draw the game
            self.screen.fill((0, 0, 0))
            self.draw_grid(self.screen)
            if self.reached_goal:
                self.show_end_message()
            pygame.display.flip()

        pygame.quit()
        print("Number of steps used:", game.get_num_steps())


    def get_num_steps(self):
        """Getter for the number of steps used so far."""
        return self.num_steps


    def get_ascii_game_world(self):
        """
        Returns a simple ASCII representation of the world, 
        including the outer boundary as '#' characters.

        Legend:
          '#' = wall or boundary
          'S' = start
          'G' = goal
          'P' = player
          ' ' = empty cell
        """
        lines = []

        # Top boundary (grid_size + 2 for corners)
        lines.append('#' * (self.grid_size + 2))

        for row in range(self.grid_size):
            # Start with left boundary
            row_chars = ['#']

            for col in range(self.grid_size):
                # Player takes priority
                if (col, row) == (self.player_x, self.player_y):
                    row_chars.append('P')
                else:
                    cell_value = self.map_data[row][col]
                    if cell_value == WALL:
                        row_chars.append('#')
                    elif cell_value == START:
                        row_chars.append('S')
                    elif cell_value == GOAL:
                        row_chars.append('G')
                    else:
                        row_chars.append(' ')
            
            # Right boundary
            row_chars.append('#')
            lines.append("".join(row_chars))

        # Bottom boundary
        lines.append('#' * (self.grid_size + 2))

        return "\n".join(lines)

    def get_image_game_world(self, step_count: int):
        """
        Returns a PyGame Surface with the current game state drawn on it,
        effectively a 'screenshot' of the grid in its current state.
        """
        temp_surface = pygame.Surface((self.width, self.height))
        self.draw_grid(temp_surface)
        
        img_dir = "./img_game_states"
        os.makedirs(img_dir, exist_ok=True)
        filename = f'game_state_{step_count}.png'
        file_path = os.path.join(img_dir, filename)
        
        pygame.image.save(temp_surface, file_path)
        
        return file_path