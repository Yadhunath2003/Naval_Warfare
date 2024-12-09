from game_logic import GameBoard  # Import the GameBoard for board management
import random

GRID_SIZE = 10

class Player:
    def __init__(self, name):
        self.name = name
        self.board = GameBoard(10, 10)  # Create a new 10x10 board for the player
        self.hits = []  # Coordinates of successful hits
        self.misses = []  # Coordinates of missed attacks

    def place_ships(self, ships):
        """
        Places ships on the player's board.
        ships: List of tuples containing ship data (length, orientation, start_position).
        """
        for ship_length, orientation, start_position in ships:
            self.board.place_ship(ship_length, orientation, start_position)

    def attack(self, opponent, x, y):
        """
        Perform an attack on the opponent's board.
        opponent: The opposing Player object.
        x, y: Coordinates of the attack.
        Returns True if it's a hit, False if it's a miss.
        """
        if opponent.board.grid[y][x] == "S":  # "S" marks a ship
            self.hits.append((x, y))
            opponent.board.grid[y][x] = "X"  # Mark as hit
            return True  # Hit
        else:
            self.misses.append((x, y))
            opponent.board.grid[y][x] = "O"  # Mark as miss
            return False  # Miss

class AIPlayer(Player):
    def __init__(self, name, difficulty, num_boats):
        super().__init__(name)
        self.difficulty = difficulty  # Assign the difficulty level to the instance

    def make_move(self, opponent_board):
        """
        Make a move based on AI difficulty level.
        opponent_board: The board of the opponent to attack.
        Returns the coordinates (x, y) of the move.
        """
        if self.difficulty == "Easy":
            return self.easy_move(opponent_board)
        elif self.difficulty == "Medium":
            return self.medium_move(opponent_board)
        elif self.difficulty == "Hard":
            return self.hard_move(opponent_board)

    def easy_move(self, opponent_board):
        """
        Easy mode: Randomly selects an unplayed cell.
        """
        available_moves = [
            (x, y)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if not opponent_board.is_attacked(x, y)
        ]
        return random.choice(available_moves) if available_moves else (None, None)

    def medium_move(self, opponent_board):
        """
        Medium mode: Targets surrounding cells of a previous hit.
        """
        for x, y in self.hits:
            potential_targets = [
                (x + dx, y + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE and not opponent_board.is_attacked(x + dx, y + dy)
            ]
            if potential_targets:
                return random.choice(potential_targets)
        return self.easy_move(opponent_board)

    def hard_move(self, opponent_board):
        """
        Hard mode: Directly targets ship cells if known, otherwise falls back to easy_move.
        """
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if opponent_board.grid[x][y] == "S" and not opponent_board.is_attacked(x, y):
                    return x, y
        return self.easy_move(opponent_board)
