'''
Author: Isabel Loney
Creation Date: September 11, 2024
Last Modified: September 15, 2024
Commenting: Provide prologue comments for each function specifying input, output, and a description, as well as any notes/TODOs
            Provide inline comments for sections of code within functions to clarify functionality and purpose. Written on 9/15/24
Program Name: Battleship - player.py
Purpose: Player Class that stores player information and provides methods for player interaction
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py for class and method structure (i.e. method names, class name)
Other collaborators: Code reviewed and tested by Jackson Wunderlich
'''
# All code written by Isabel Loney
from board import Board
from ship import Ship

class Player:
    # Input: Player name ("Player 1" or "Player 2") and a list of ships
    # Output: A player object
    # Description: Player Object constructor
    def __init__(self, player_name, fleet):
        self.player_name = player_name
        self.board = Board()
        self.fleet = fleet # list of fleet of ships. depends on what is chosen for the game by users. see Game.py
        self.opponent = None
    
    # Input: Player object
    # Output: None
    # Description: Sets the oppenent
    def set_opponent(self, opponent):
        self.opponent = opponent
    
    # Inputs: None; Player is provided ships on creation
    # Outputs: None
    # Description: position ships with for loop of place_ships + board confirmation to finalize board
    def place_fleet(self):
        print(f"{self.player_name}'s turn to place ships")
        print(f"No cheating, {self.opponent.player_name}! Look away!")
        input("Press enter to begin")
        
        accepted = False
        while not accepted:
            for ship in self.fleet:
                # keep prompting to place a ship until a valid position is given
                while self.place_ship(ship) == False:
                    continue
            # once fleet is placed, print board to for user to confirm everything is as desired
            print(self.board.player_view())
            prompt = input("Is this board okay?:\n 1. Yes\n 2. No\nChoice: ").strip()
            if prompt == '1':
                accepted = True
            # anything besides 'yes' is considered as 'no'
            else:
                print("Resetting board")
                # clear board
                self.board.grid = [[" _" for i in range(10)] for i in range(10)]
                print("Board reset")
        # clear all previous text
        print("\033[H\033[J", end="")
        
    
    # Input: a single ship
    # Output: Boolean indicating whether placing the ship was successful
    # Description: Prompt players for orientation and top left position of ship, then attempt to place ship based on those requests
    def place_ship(self, ship):
        # constants
        HORIZONTAL_SELECTED = '1'
        VERTICAL_SELECTED = '2'

        # show board as is 
        print("Current board: ")
        print(self.board.player_view())

        print("Placing ship with length ", ship.size)
        # ask orientation horizontal or vertical
        valid_orientation_selected = False
        # keep prompting for orientation until '1' or '2' is entered
        # then set orientation
        while not valid_orientation_selected:
            orientation = input("Choose Orientation:\n 1. Horizontal\n 2. Vertical \nPlayer choice: ").strip()
            if orientation == HORIZONTAL_SELECTED:
                ship.set_orientation('horizontal')
                valid_orientation_selected = True
            elif orientation == VERTICAL_SELECTED:
                ship.set_orientation('vertical')
                valid_orientation_selected = True
            else:
                print("Invalid orientation")


        # prompt for and set top left position of boat
        col_valid = False
        col = ''
        # keep prompting until valid column given
        while not col_valid:
            col = input("Enter column from A-J: ").strip()
            # Python supports comparisons of strings based on their ASCII number, so this is okay despite how strange it looks
            # only accept 1 letter answers to avoid any confusion
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
                # gives a number 0-10 ('a' ascii value is 97, successive letters go up by 1 in alphabetical order)
                ship.x = ord(col.lower()) - 97
                col_valid = True
            else:
                print("Invalid column")
        
        # keep prompting until row column given
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
            # non-integer provided
            except ValueError:
                print("Invalid row number")


        # use place_ship from board.py
        return self.board.place_ship(ship)

    # Input: The type of fleet, which indicates size and number of ships
    # Output: boolean indicating whether the current player has won
    # Description: prompt for position on board and attack
    # Does not check if position has already been attacked
    def take_turn(self, fleet_type):
        # check if p1/p2 ready
        print(f"{self.player_name}'s turn to attack")
        print(f"No cheating, {self.opponent.player_name}! Look away!")
        input("Press enter to begin turn")

        # display boards - player board and opponent board with hits/misses shown and ships hidden
        print("Your board")
        print(self.board.player_view())
        print("Opponent's board")
        print(self.opponent.board.opponent_view())

        # prompt for place to attack
        col_valid = False
        col = ''
        # keep prompting until valid column given
        while not col_valid:
            col = input("Enter column from A-J: ").strip()
            # Python supports comparisons of strings based on their ASCII number, so this is okay despite how strange it looks
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
                # gives a number 0-10 ('a' ascii value is 97, successive letters go up by 1 in alphabetical order)
                col = ord(col.lower()) - 97
                col_valid = True
            else:
                print("Invalid column")
        
        row_valid = False
        row = 0
        # keep prompting until valid row given
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

        # attack and indiciate if hit or miss
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
