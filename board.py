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
        result = "" #initialize empty string for board
        for row in self.grid: #iterates through eaech row
            for space in row: #iterates through each space in row
                result+=space+ " " #adds space in grid
            result+= "\n" #adds new line at end of row
        return result

        
    # string grid with hidden ship locations for opponent
    def opponent_view(self):
        result = "" # intialize empty string for board
        for row in self.grid: #iterate through each row
            for space in row: #iterates through eaech space in the row
                if space == ' S': #if the space contains a ship it will hide it
                    result += ' _ ' #hids ship with empty space
                else:
                    result += space + " " #otherwise just returns the emtpy space
        return result
  
    
    #string grid with player's own view with ships visible
    def player_view(self):
        self.__str__() 
    
    

    # place ship on board, check for legal positioning of ship as well
    def place_ship(self, ship):
        pass

    # attack method, record attack whether hit or miss. takes in x,y position on board
    def attack(self, x, y):
        # if position is an "S", then mark as hit "x"
        # you get the gist..
        pass
    
    # check if player has lost
    def defeat(self):
        # can use the hit_count
        pass



