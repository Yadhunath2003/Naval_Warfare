import random
from player import Player

class AIPlayer(Player):
    def __init__(self, difficulty, board, fleet):
        # Initialize the AI player with difficulty level, game board, and fleet of ships.
        super().__init__(board, fleet)
        self.difficulty = difficulty
        self.last_hit = None  # Track the last successful hit for targeted firing
        # Create a list of possible moves on the board and shuffle it for randomness
        self.possible_moves = [(x, y) for x in range(10) for y in range(10)]
        random.shuffle(self.possible_moves)
        self.adjacent_moves = []  # Initialize a list to store adjacent moves after a hit

    def place_ships(self):
        # Randomly place each ship from the fleet on the board
        for ship in self.fleet:
            placed = False
            while not placed:
                row = random.randint(0, 9)  # Random row selection
                col = random.randint(0, 9)  # Random column selection
                orientation = random.choice(['H', 'V'])  # Randomly choose orientation (horizontal or vertical)
                # Attempt to place the ship on the board
                placed = self.board.place_ship(ship, row, col, orientation)

    def fire(self):
        # Determine firing strategy based on difficulty level
        if self.difficulty == 'Easy':
            return self.fire_random()  # Fire randomly for easy difficulty
        elif self.difficulty == 'Medium':
            if self.last_hit:
                return self.fire_near_last_hit()  # Attempt to hit near the last successful hit
            else:
                return self.fire_random()  # Fire randomly if no last hit
        elif self.difficulty == 'Hard':
            return self.cheat_fire()  # Use knowledge of the board to target ships for hard difficulty

    def fire_random(self):
        # Execute a random attack on the board
        move = self.possible_moves.pop()  # Get a random move from the list of possible moves
        row, col = move
        result = self.board.attack(col, row)  # Attack the specified coordinates
        if result:
            self.last_hit = (row, col)  # Update last hit if the attack is successful
        return move, result  # Return the move and the attack result

    def fire_near_last_hit(self):
        # Fire at locations adjacent to the last hit
        if not self.adjacent_moves:
            self.adjacent_moves = self.get_adjacent_moves(self.last_hit)  # Get adjacent moves if none exist
        next_move = self.adjacent_moves.pop(0)  # Get the next adjacent move
        row, col = next_move
        result = self.board.attack(col, row)  # Attack the specified coordinates
        if result:
            self.last_hit = (row, col)  # Update last hit if successful
        return next_move, result  # Return the next move and the attack result

    def get_adjacent_moves(self, move):
        # Generate valid moves that are adjacent to the last hit
        row, col = move
        potential_moves = [
            (row - 1, col), (row + 1, col),  # Up and down moves
            (row, col - 1), (row, col + 1)   # Left and right moves
        ]
        # Filter potential moves to ensure they are within the board boundaries
        valid_moves = [m for m in potential_moves if 0 <= m[0] < 10 and 0 <= m[1] < 10]
        random.shuffle(valid_moves)  # Shuffle valid moves for randomness
        return valid_moves  # Return the list of valid adjacent moves

    def cheat_fire(self):
        # Directly attack locations where ships are present (used in hard difficulty)
        for row in range(10):
            for col in range(10):
                if self.board.grid[row][col] == "S":  # Check if the cell contains a ship ("S")
                    self.board.attack(col, row)  # Attack the cell with the ship
                    return (row, col), True  # Return the coordinates of the attack and indicate success
