from board import Board

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        # self.fleet = list of fleet of ships. dependds on what is chosen for the game by users.. see Game.py
        self.opponent = None
    
    def set_opponent(self, opponent): # may not need this?
        self.opponent = opponent
    
    def place_fleet(self):
        # position ships with for loop of place_ships
        # board confirmation to finalize board
        pass
    
    def place_ship(self, ship):
        # show board as is 

        # ask orientation horizontal or vertical

        # prompt for top left position of boat. while loop
        # use place_ship from board.py
        pass

    def take_turn(self):
        # display boards (handle public and private boards). check if p1/p2 ready

        # prompt for place to attack

        # do attack and indiciate if hit or miss

        # check for opponent defeat
        pass
