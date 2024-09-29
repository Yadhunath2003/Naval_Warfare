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
        self.fleet = fleet  # list of fleet of ships. depends on what is chosen for the game by users. see Game.py
        self.opponent = None
        self.hits = 0  # Added to track player hits
        self.misses = 0  # Added to track player misses

    # Input: Player object
    # Output: None
    # Description: Sets the opponent
    def set_opponent(self, opponent):
        self.opponent = opponent

    # Inputs: None; Player is provided ships on creation
    # Outputs: None
    # Description: position ships with for loop of place_ships + board confirmation to finalize board
    def place_fleet(self):
        print(f"{self.player_name}'s turn to place ships")
        print(f"No cheating,\n{self.opponent.player_name}! Look away!")
        input("Press enter to begin")
        
        accepted = False
        while not accepted:
            for ship in self.fleet:
                while self.place_ship(ship) == False:
                    continue
            print(self.board.player_view())
            prompt = input("Is this board okay?:\n 1. Yes\n 2. No\nChoice: ").strip()
            if prompt == '1':
                accepted = True
            else:
                print("Resetting board")
                self.board.grid = [[" _" for i in range(10)] for i in range(10)]
                print("Board reset")
        print("\033[H\033[J", end="")

    def place_ship(self, ship):
        HORIZONTAL_SELECTED = '1'
        VERTICAL_SELECTED = '2'

        print("Current board: ")
        print(self.board.player_view())
        print("Placing ship with length ", ship.size)

        valid_orientation_selected = False
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

        col_valid = False
        col = ''
        while not col_valid:
            col = input("Enter column from A-J: ").strip()
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
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
                    ship.y = row-1
                    row_valid = True
            except ValueError:
                print("Invalid row number")

        return self.board.place_ship(ship)

    def take_turn(self, fleet_type):
        print(f"{self.player_name}'s turn to attack")
        print(f"No cheating, {self.opponent.player_name}! Look away!")
        input("Press enter to begin turn")

        print("Your board")
        print(self.board.player_view())
        print("Opponent's board")
        print(self.opponent.board.opponent_view())

        col_valid = False
        col = ''
        while not col_valid:
            col = input("Enter column from A-J: ").strip()
            if (col >= 'A' and col <= 'J') or (col >= 'a' and col <= 'j') and (len(col) < 2):
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
                    row = row-1
                    row_valid = True
            except ValueError:
                print("Invalid row number")

        if self.opponent.board.attack(col, row):
            print("Hit!")
            self.hits += 1  # Track hit
        else:
            print("Miss!")
            self.misses += 1  # Track miss

        if self.opponent.board.defeat(fleet_type):
            return True
        else:
            input("Press enter to end turn")
            print("\033[H\033[J", end="")
            return False
