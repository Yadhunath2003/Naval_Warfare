class Board:
    # Ships: space that contains ship: denoted as "S" (or s1 or s2 for players one or two.. depends)
    # Empty: space w no ship: denoted _
    # Hit: space that used to be ship, was hit: denoted as "X"
    # Miss: space attacked, but no hit: denoted as "O"
    def __init__(self):
        # grid
        self.grid([" _" for i in range(10)])
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



