"""Authors: Kemar and Yadhunath
    Created: 11/8/2024
    Last updated: 11/10/2024
    This the ai function that contains all the important functions for the 3 AI modes.
    It also includes some aspects of the board class of the placement, and they would be incorporated in the upcoming sprints to the main game.
    This majoritily deals with backend declaration of the ai modes.
    
    Future changes would be made when we incorporate it with the board."""


import random

GRID_SIZE = 10  
"""This class would be later replaced with the fully functional boat class."""
class Boat:
    def __init__(self, length):
        self.length = length
        self.positions = []

class Board:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.boats = []

    def place_boat(self, boat):
        placed = False
        while not placed:
            orientation = random.choice(["H", "V"])
            if orientation == "H":
                x = random.randint(0, GRID_SIZE - boat.length)
                y = random.randint(0, GRID_SIZE - 1)
                if all(self.grid[x + i][y] == 0 for i in range(boat.length)):
                    for i in range(boat.length):
                        self.grid[x + i][y] = 1
                        boat.positions.append((x + i, y))
                    placed = True
            else:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - boat.length)
                if all(self.grid[x][y + i] == 0 for i in range(boat.length)):
                    for i in range(boat.length):
                        self.grid[x][y + i] = 1
                        boat.positions.append((x, y + i))
                    placed = True

    def place_ai_boats(self, num_boats):
        for _ in range(num_boats):
            boat_length = random.randint(2, 5)
            boat = Boat(boat_length)
            self.place_boat(boat)
            self.boats.append(boat)

    def is_hit(self, x, y):
        return self.grid[x][y] == 1

class AIPlayer:
    def __init__(self, difficulty, num_boats):
        self.difficulty = difficulty
        self.board = Board()
        self.board.place_ai_boats(num_boats)

    def make_move(self, opponent_board):
        if self.difficulty == "Easy":
            return self.easy_move(opponent_board)
        elif self.difficulty == "Medium":
            return self.medium_move(opponent_board)
        elif self.difficulty == "Hard":
            return self.hard_move(opponent_board)

    def easy_move(self, opponent_board):
        """
        AI selects a random cell that has not been attacked yet.
        """
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if opponent_board.grid[y][x] == 0:  # Ensure the cell is unvisited
                return x, y

    def medium_move(self, opponent_board):
        """
        AI improves its targeting logic:
        - If there's a hit, attack adjacent cells.
        - Otherwise, pick a random unvisited cell.
        """
        # Find all cells that have been hit but not yet sunk
        hits = [
            (x, y)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if opponent_board.grid[y][x] == 2  # 2 indicates a hit
        ]

        # If there are hits, target adjacent cells
        if hits:
            last_hit = hits[-1]
            x, y = last_hit
            potential_targets = [
                (x + dx, y + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Adjacent cells
                if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE
                and opponent_board.grid[y + dy][x + dx] == 0  # Ensure unvisited
            ]
            if potential_targets:
                return random.choice(potential_targets)

        # Default to random unvisited cell
        return self.easy_move(opponent_board)

    def hard_move(self, opponent_board):
        """
        AI implements strategic targeting:
        - Prioritize finishing off partially-hit ships.
        - Uses a probability-based heatmap for efficient hunting.
        """
        # Find all cells that have been hit but not yet sunk
        hits = [
            (x, y)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if opponent_board.grid[y][x] == 2  # 2 indicates a hit
        ]

        # Prioritize finishing ships by targeting adjacent cells
        if hits:
            for hit in hits:
                x, y = hit
                potential_targets = [
                    (x + dx, y + dy)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Adjacent cells
                    if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE
                    and opponent_board.grid[y + dy][x + dx] == 0  # Ensure unvisited
                ]
                if potential_targets:
                    return random.choice(potential_targets)

        # Use a simple heuristic for hunting ships
        # Target every other cell for more efficient searching
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x + y) % 2 == 0 and opponent_board.grid[y][x] == 0:
                    return x, y

        # Fallback to random move if all else fails
        return self.easy_move(opponent_board)

