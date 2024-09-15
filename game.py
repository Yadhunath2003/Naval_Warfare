'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - ship.py
Purpose: Create and run battleship game
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich
'''
# Code structure adapted from https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py BattleshipGame class and modified for this projects purposes
# Code written by Anakha Krishna
from player import Player
from ship import Ship

class Game:
    # Input: None
    # Output: A game object
    # Description: Game object constructor
    def __init__(self):
        self.fleet_options = { # create lists of fleet types
            1: [Ship(1)],
            2: [Ship(1), Ship(2)],
            3: [Ship(1), Ship(2), Ship(3)],
            4: [Ship(1), Ship(2), Ship(3), Ship(4)],
            5: [Ship(1), Ship(2), Ship(3), Ship(4), Ship(5)]
        }
        self.fleet_type = None # chosen fleet type 

    # Input: Player input specifying when to begin turn, where to place ships, and where to attack
    # Output: The player's own board and an onfuscated view of the opponent's board
    # Description: method to run the game, position boats, attack, and alternate turns until a player wins
    def play(self):
        print("Welcome to Battleship!")
        chosen_fleet = None
        while chosen_fleet is None: # Prompt for fleet type until valid fleet type is givens
            try:
                fleet_type = int(input("Choose a fleet type (1, 2, 3, 4, or 5): ")) # prompt user for fleet type
                if fleet_type in self.fleet_options: # if valid input,
                    chosen_fleet = self.fleet_options[fleet_type] # set fleet type in chosen_fleet for player 1 use
                    chosen_fleet_copy = self.fleet_options[fleet_type] # set fleet type in chosen_fleet_copy for player 2 use
                    self.fleet_type = fleet_type # set fleet type for use in other methods
                else:
                    print("Invalid fleet type. Please choose 1, 2, 3, 4, or 5.") # handle invalid input
            except ValueError:
                print("Invalid input. Please enter a number (1, 2, 3, 4, or 5).") # handle invalid input
            
        self.players = [Player("Player 1", chosen_fleet), Player("Player 2", chosen_fleet_copy)] # create game players 

        # Set opponent (adapted from https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py)
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

        # place fleets (adapted from https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py)
        self.players[0].place_fleet()
        self.players[1].place_fleet()

        input("All ships in place. Players...are you ready? Press enter to begin the battle!") # prompt for game to start

        # game loop
        game_over = False # will handle take_turn() boolean result (True if game won, False if game continues)
        current_player_index = 0 # keeps track of which players turn it is

        while not game_over:
            current_player = self.players[current_player_index] # start with players[0]

            game_over = current_player.take_turn(self.fleet_type) # call take turn and assign to game_over

            if not game_over: # continue game if take_turn() returns false
                current_player_index = 1 - current_player_index # switch to next player's turn
        
        print(f"Game over... {self.players[current_player_index].player_name} wins!") # print winner




