
import random

class GameBoard:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = [['-' for _ in range(cols)] for _ in range(rows)]
        self.attack_grid = [['-' for _ in range(cols)] for _ in range(rows)]  # Attack results
        self.attacked_positions = set()  # Tracks all attacked positions (x, y) on this board
        self.ships = []

    def is_valid_placement(self, ship_length, orientation, start_position):
        """
        Check if a ship placement is valid.
        """
        x, y = start_position
        if orientation == 'horizontal':
            if x + ship_length > self.cols:  # Out of bounds horizontally
                return False
            for i in range(ship_length):
                if self.grid[y][x + i] != '-':  # Overlap check
                    return False
        elif orientation == 'vertical':
            if y + ship_length > self.rows:  # Out of bounds vertically
                return False
            for i in range(ship_length):
                if self.grid[y + i][x] != '-':  # Overlap check
                    return False
        return True
    
    def is_attacked(self, x, y):
        """
        Checks if a position has already been attacked on this board.
        """
        return (x, y) in self.attacked_positions

    def mark_attacked(self, x, y):
        """
        Marks a position as attacked on this board.
        """
        self.attacked_positions.add((x, y))

    def place_ship(self, ship_length, orientation, start_position):
        """
        Place a ship on the grid if valid.
        """
        if not self.is_valid_placement(ship_length, orientation, start_position):
            return False

        x, y = start_position
        ship_coordinates = []
        if orientation == 'horizontal':
            for i in range(ship_length):
                self.grid[y][x + i] = 'S'  # Assign a unique ID
                ship_coordinates.append((x + i, y))
        elif orientation == 'vertical':
            for i in range(ship_length):
                self.grid[y + i][x] = 'S'  # Assign a unique ID
                ship_coordinates.append((x, y + i))

        # Add the ship to the ships list
        self.ships.append({
            "id": len(self.ships) + 1,
            "length": ship_length,
            "orientation": orientation,
            "coordinates": ship_coordinates
        })
        return True


    def randomly_place_ships(self, ship_lengths):
        """
        Randomly place multiple ships on the grid.
        """
        for ship_length in ship_lengths:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                start_position = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
                placed = self.place_ship(ship_length, orientation, start_position)

    def display_grid(self):
        """
        Print the current state of the grid for debugging.
        """
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    def get_ship_placements(self):
        """
        Return the current grid with ship placements for display or game logic.
        """
        return [[cell for cell in row] for row in self.grid]

    def display_ship_placements(self):
        """
        Print the current grid with ship placements for debugging or display.
        """
        print("Current Ship Placements:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def update_attack_grid(self, x, y, result):
        """
        Updates the attack grid based on the attack result.
        """
        if result:  # Hit
            self.attack_grid[y][x] = 'X'
        else:  # Miss
            self.attack_grid[y][x] = 'O'

    
