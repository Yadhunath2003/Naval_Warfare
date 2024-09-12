class Board:
    # Ships: space that contains ship: denoted as "S" (or s1 or s2 for players one or two.. depends)
    # Empty: space w no ship: denoted _
    # Hit: space that used to be ship, was hit: denoted as "X"
    # Miss: space attacked, but no hit: denoted as "O"
    def __init__(self):
        # grid
        self.grid = [["_" for i in range(10)] for i in range(10)]
        # hit count
        # self.hit_count = 0

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

    # Input: a ship
    # Output: Boolean indicating if placing the ship was a success
    # Description: place ship on board
    # Notes: player.py/place_ship has already handled whether a valid top left position has been selected 
    # (TODO: that logic can and probably should be moved here but I'm too lazy to do that rn)
    # this fucntion must make sure:
    #   a. The entire ship stays on the board
    #   b. it does not intersect with ships already placed
    def place_ship(self, ship):
        if ship.orientation == 'horizontal':
            if ship.x + ship.size > 10:
                print("Could not place ship: entire ship must be on the board")
                return False
            
            collision_area = self.grid[ship.y][ship.x:(ship.x+ship.size)]
            if 'S' in collision_area:
                print("Could not place ship: overlaps with previously placed ship")
                return False
            
            for i in range(ship.x, ship.x+ship.size):
                self.grid[ship.y][i] = 'S'
            return True

        elif ship.orientation == 'vertical':
            if ship.y + ship.size > 10:
                print("Could not place ship: entire ship must be on the board")
                return False
            
            collision_area = [self.grid[i][ship.x] for i in range(ship.y, ship.y+ship.size)]
            if 'S' in collision_area:
                print("Could not place ship: overlaps with previously placed ship")
                return False
            
            for i in range(ship.y, ship.y+ship.size):
                self.grid[i][ship.x] = 'S'
            return True

    # attack method, record attack whether hit or miss. takes in x,y position on board
    def attack(self, x, y):
        # if position is an "S", then mark as hit "x"
        # you get the gist..
        pass
    
    # check if player has lost
    def defeat(self):
        # can use the hit_count
        pass



