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
        # Add hits and misses attributes
        self.hits = []
        self.misses = []
    def make_move(self, opponent_board):
        if self.difficulty == "Easy":
            x, y = self.easy_move(opponent_board)
        elif self.difficulty == "Medium":
            x, y = self.medium_move(opponent_board)
        elif self.difficulty == "Hard":
            x, y = self.hard_move(opponent_board)
        else:
            raise ValueError("Invalid difficulty level")
        # Check if the move hits or misses
        if opponent_board.is_hit(x, y):
            self.hits.append((x, y))
            opponent_board.grid[x][y] = 2  # Mark as hit
        else:
            self.misses.append((x, y))
            opponent_board.grid[x][y] = -1  # Mark as miss
        return x, y

    def easy_move(self, opponent_board):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while opponent_board.grid[x][y] == -1:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        return x, y

    def medium_move(self, opponent_board):
        hits = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if opponent_board.grid[x][y] == 2]
        if hits:
            last_hit = hits[-1]
            x, y = last_hit
            options = [(x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
            options = [(x, y) for x, y in options if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and opponent_board.grid[x][y] == 0]
            if options:
                return random.choice(options)
        return self.easy_move(opponent_board)

    def hard_move(self, opponent_board):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if opponent_board.is_hit(x, y) and opponent_board.grid[x][y] != -1:
                    return x, y
        return self.easy_move(opponent_board)
