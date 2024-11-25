from game_logic import GameBoard  # Import the GameBoard for board management

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
