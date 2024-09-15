from game import Game

class Board:
    # Ships: space that contains ship: denoted as "S" (or s1 or s2 for players one or two.. depends)
    # Empty: space w no ship: denoted _
    # Hit: space that used to be ship, was hit: denoted as "X"
    # Miss: space attacked, but no hit: denoted as "O"
    def __init__(self):
        # grid
        self.grid = [[" _" for _ in range(10)] for _ in range(10)] #creates 10x10 grid with empty spaces
        # hit count
        self.hit_count = 0 #sets hit count to zero and intializes it 
    

    # string representation of grid
    def __str__(self): 
        result = "    A  B  C  D  E  F  G  H  I  J\n"  # Add column labels (A-J)
        for i, row in enumerate(self.grid, 1):  #iterates through eaech row starting at 1 and labels it
            result += f"{i:2} " 
            for space in row: #iterates through each space in row
                result+=space+ " " #adds space in grid
            result+= "\n" #adds new line at end of row
        return result

        
    # string grid with hidden ship locations for opponent
    def opponent_view(self):
        result = "    A  B  C  D  E  F  G  H  I  J\n"  # Add column labels (A-J)
        for i, row in enumerate(self.grid, 1):  #iterates through eaech row starting at 1 and labels it
            result += f"{i:2} "
            for space in row: #iterates through eaech space in the row
                if space == ' S': #if the space contains a ship it will hide it
                    result += ' _ ' #hids ship with empty space
                else:
                    result += space + " " #otherwise just returns the emtpy space
        return result
  
    
    #string grid with player's own view with ships visible
    def player_view(self):
        return self.__str__() 
    
    

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
            if ' S' in collision_area:
                print("Could not place ship: overlaps with previously placed ship")
                return False
            
            for i in range(ship.x, ship.x+ship.size):
                self.grid[ship.y][i] = ' S'
            return True

        elif ship.orientation == 'vertical':
            if ship.y + ship.size > 10:
                print("Could not place ship: entire ship must be on the board")
                return False
            
            collision_area = [self.grid[i][ship.x] for i in range(ship.y, ship.y+ship.size)]
            if ' S' in collision_area:
                print("Could not place ship: overlaps with previously placed ship")
                return False
            
            for i in range(ship.y, ship.y+ship.size):
                self.grid[i][ship.x] = ' S'
            return True

    # attack method, record attack whether hit or miss. takes in x,y position on board
    def attack(self, x, y):
        position = self.grid[y][x] # checks what's currently at the position
        if position == " S": # if there's a ship at the position 
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
