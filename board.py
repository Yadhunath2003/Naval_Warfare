from player import Player
from game import Game

class Board:
    # Ships: space that contains ship: denoted as "S" (or s1 or s2 for players one or two.. depends)
    # Empty: space w no ship: denoted _
    # Hit: space that used to be ship, was hit: denoted as "X"
    # Miss: space attacked, but no hit: denoted as "O"
    def __init__(self):
        # grid
        self.grid([" _" for i in range(10)])
        # hit count
        self.hit_count = 0
        self.game = Game()

    # string representation of grid
    def __str__(self):
        pass

    # string grid with hidden ship locations for opponent
    def opponent_view(self):
        pass
    
    #string grid with player's own view with ships visible
    def player_view(self):
        # prob just self.board ...may not be needed
        pass

    # place ship on board, check for legal positioning of ship as well
    def place_ship(self, ship):
        pass

    # attack method, record attack whether hit or miss. takes in x,y position on board
    def attack(self, x, y):
        position = self.grid[y][x] # checks what's currently at the position
        if position == "S": # if there's a ship at the position 
            self.grid[y][x] = " X" # changes the position from 'S' to 'X' indicating a hit
            self.hit_count += 1 # adds one to the hit count to use later 
            return True # communicates back that there was a hit
        elif position == " _": # if there isn't a ship in this position
            self.grid[y][x] = " O" # changes the position from 'S' to 'X' indicating a miss
            return False # communicates back that there wasn't a hit
        else: # returns false if both cases above don't work
            return False
    
    # check if player has lost
    def defeat(self):
        fleet_hit_counts = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15} # this assigns the fleet sizes (1 - 5) with the number of ship hit points they'll have
        return self.hit_count == fleet_hit_counts.get(Game.fleet_type, 0) # checks if the hit_count matches the required number of hits to defeat the fleet, depending on the value from Game.fleet_type
