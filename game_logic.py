
import random

class GameBoard:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
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
                if self.grid[y][x + i] != 0:  # Overlap check
                    return False
        elif orientation == 'vertical':
            if y + ship_length > self.rows:  # Out of bounds vertically
                return False
            for i in range(ship_length):
                if self.grid[y + i][x] != 0:  # Overlap check
                    return False
        return True

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
                self.grid[y][x + i] = len(self.ships) + 1  # Assign a unique ID
                ship_coordinates.append((x + i, y))
        elif orientation == 'vertical':
            for i in range(ship_length):
                self.grid[y + i][x] = len(self.ships) + 1  # Assign a unique ID
                ship_coordinates.append((x, y + i))

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

# Example Usage
if __name__ == "__main__":
    board = GameBoard()
    ship_lengths = [5, 4, 3, 2, 1]
    board.randomly_place_ships(ship_lengths)
    board.display_grid()

    print("Ships:")
    for ship in board.ships:
        print(ship)
