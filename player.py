from board import Board
from ship import Ship

class Player:
    def __init__(self, player_name, fleet):
        self.player_name = player_name
        self.board = Board()
        self.fleet = fleet # list of fleet of ships. depends on what is chosen for the game by users. see Game.py
        self.opponent = None
    
    def set_opponent(self, opponent):
        self.opponent = opponent
    
    # Inputs: None; Player is provided ships on creation
    # Outputs: None
    # Description:  position ships with for loop of place_ships + board confirmation to finalize board
    def place_fleet(self):
        print(f"{self.player_name}'s turn to place ships")
        print(f"No cheating, {self.opponent.player_name}! Look away!")
        input("Press enter to begin")
        
        accepted = False
        while not accepted:
            for ship in self.fleet:
                while self.place_ship(ship) == False:
                    continue
            print(self.board.player_view())
            prompt = input("Is this board okay?:\n 1. Yes\n 2. No\nChoice: ")
            if prompt == '1':
                accepted = True
            else:
                print("Resetting board")
                self.board.grid = [[" _" for i in range(10)] for i in range(10)]
                print("Board reset")
        # clear all previous text
        print("\033[H\033[J", end="")

        
    
    # Input: a ship
    # Output: Boolean indicating whether placing the ship was successful
    # Description: Prompt players for orientation and top left position of ship, then attempt to place ship based on those requests
    def place_ship(self, ship):
        HORIZONTAL_SELECTED = '1'
        VERTICAL_SELECTED = '2'
        # show board as is 
        print("Current board: ")
        print(self.board.player_view())

        print("Placing ship with length ", ship.size)
        # ask orientation horizontal or vertical
        valid_orientation_selected = False
        while not valid_orientation_selected:
            orientation = input("Choose Orientation:\n 1. Horizontal\n 2. Vertical \nPlayer choice: ")
            if orientation == HORIZONTAL_SELECTED:
                ship.orientation = 'horizontal'
                valid_orientation_selected = True
            elif orientation == VERTICAL_SELECTED:
                ship.orientation = 'vertical'
                valid_orientation_selected = True
            else:
                print("Invalid orientation")


        # prompt for top left position of boat

        col_valid = False
        col = ''
        while not col_valid:
            col = input("Enter column from A-J: ")
            # Python supports comparisons of strings based on their ASCII number, so this is okay despite how strange it looks
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
                # gives a number 0-10 ('a' ascii value is 97, successive letters go up by 1 in alphabetical order)
                ship.x = ord(col.lower()) - 97
                col_valid = True
            else:
                print("Invalid column")
        
        row_valid = False
        row = 0
        while not row_valid:
            try:
                row = int(input("Enter row from 1-10: "))
                if row < 1 or row > 10:
                    print("Invalid row number")
                else:
                    # -1 to make it easier to work with 0-indexed lists
                    ship.y = row-1
                    row_valid = True
            except ValueError:
                print("Invalid row number")


        # use place_ship from board.py
        return self.board.place_ship(ship)

    # Input: None
    # Output: boolean indicating whether the current player has won
    # Description: prompt for position on board and attack
    # TODO(?): Check if position has already been attacked?
    def take_turn(self, fleet_type):
        # check if p1/p2 ready
        print(f"{self.player_name}'s turn to attack")
        print(f"No cheating, {self.opponent.player_name}! Look away!")
        input("Press enter to begin turn")

        # display boards (handle public and private boards).
        print("Your board")
        print(self.board.player_view())
        print("Opponent's board")
        print(self.opponent.board.opponent_view())

        # prompt for place to attack

        col_valid = False
        col = ''
        while not col_valid:
            col = input("Enter column from A-J: ")
            # Python supports comparisons of strings based on their ASCII number, so this is okay despite how strange it looks
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
                # gives a number 0-10 ('a' ascii value is 97, successive letters go up by 1 in alphabetical order)
                col = ord(col.lower()) - 97
                col_valid = True
            else:
                print("Invalid column")
        
        row_valid = False
        row = 0
        while not row_valid:
            try:
                row = int(input("Enter row from 1-10: "))
                if row < 1 or row > 10:
                    print("Invalid row number")
                else:
                    # -1 to make it easier to work with 0-indexed lists
                    row = row-1
                    row_valid = True
            except ValueError:
                print("Invalid row number")

        # do attack and indiciate if hit or miss
        if (self.opponent.board.attack(col, row)):
            print("Hit!")
        else:
            print("Miss!")

        # check for opponent defeat
        if self.opponent.board.defeat(fleet_type):
            return True
        else:
            # game continues
            # clear all previous text
            input("Press enter to end turn")
            print("\033[H\033[J", end="")
            return False


