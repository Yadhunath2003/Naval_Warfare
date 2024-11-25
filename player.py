class Player:
    def __init__(self, name, screen, offset=(0, 0)):
        pass

    def set_opponent(self, opponent):
        pass

    def place_fleet(self, fleet_sizes):
        pass

    def is_valid_placement(self, x, y, size, orientation):
        pass

    def add_ship(self, x, y, size, orientation):
        pass

    def draw_board(self):
        pass

    def draw_ships(self):
        pass

    def take_turn(self):
        pass

    def attack(self, x, y):
        pass

    def is_defeated(self):
        pass

    def highlight_placement(self, x, y, size, orientation):
        pass

    def highlight_attack(self, x, y):
        pass
