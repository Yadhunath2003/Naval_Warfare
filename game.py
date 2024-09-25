'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - game.py
Purpose: Create and run the Battleship game
Source(s):
https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich
'''
from player import Player
from ai_player import AIPlayer  # Import the AIPlayer class
from ship import Ship
import copy  # To ensure fleet copies are deep copies
class Game:
   # Input: player1 and player2 objects, which can be either human (Player) or AI (AIPlayer)
   # Output: A game object
   # Description: Game object constructor
   def __init__(self, player1=None, player2=None):
       # Create lists of fleet types without ship names (only sizes)
       self.fleet_options = {
           1: [Ship(1)],
           2: [Ship(1), Ship(2)],
           3: [Ship(1), Ship(2), Ship(3)],
           4: [Ship(1), Ship(2), Ship(3), Ship(4)],
           5: [Ship(1), Ship(2), Ship(3), Ship(4), Ship(5)]
       }
       self.fleet_type = None  # Chosen fleet type
       self.players = [player1, player2]  # Support for AI or human players
   # Input: Player input specifying when to begin turn, where to place ships, and where to attack
   # Output: The player's board and an obfuscated view of the opponent's board
   # Description: Run the game, position boats, attack, and alternate turns until a player wins
   def play(self):
       print("Welcome to Battleship!")
       chosen_fleet = None
       while chosen_fleet is None:  # Prompt for fleet type until valid fleet type is given
           try:
               fleet_type = int(input("Choose how many ships will be in your fleet (1, 2, 3, 4, or 5): "))  # Prompt user for fleet type
               if fleet_type in self.fleet_options:  # If valid input,
                   chosen_fleet = self.fleet_options[fleet_type]  # Set fleet type for player 1
                   chosen_fleet_copy = copy.deepcopy(self.fleet_options[fleet_type])  # Deep copy for player 2 to avoid reference issues
                   self.fleet_type = fleet_type  # Set fleet type for future use
               else:
                   print("Invalid fleet type. Please choose 1, 2, 3, 4, or 5.")  # Handle invalid input
           except ValueError:
               print("Invalid input. Please enter a number (1, 2, 3, 4, or 5).")  # Handle invalid input
       # If players were not provided (human vs human mode)
       if self.players[0] is None or self.players[1] is None:
           opponent_type = input("Do you want to play against a human or AI? (human/AI): ").strip().lower()
           if opponent_type == "ai":
               difficulty = input("Select AI difficulty (Easy/Medium/Hard): ").strip().capitalize()
               self.players[0] = Player("Player 1", chosen_fleet)  # Player 1 is always human
               self.players[1] = AIPlayer(difficulty, self.players[0].board, chosen_fleet_copy)  # Player 2 is AI
           else:
               self.players = [Player("Player 1", chosen_fleet), Player("Player 2", chosen_fleet_copy)]  # Both human players
       # Set opponent
       self.players[0].set_opponent(self.players[1])
       self.players[1].set_opponent(self.players[0])
       # Place fleets
       self.players[0].place_fleet()
       self.players[1].place_fleet()
       input("All ships in place. Players...are you ready? Press enter to begin the battle!")  # Prompt for game to start
       # Game loop
       game_over = False  # Will handle take_turn() boolean result (True if game won, False if game continues)
       current_player_index = 0  # Keeps track of which player's turn it is
       while not game_over:
           current_player = self.players[current_player_index]  # Start with players[0]
           game_over = current_player.take_turn(self.fleet_type)  # Call take_turn and assign to game_over
           if not game_over:  # Continue game if take_turn() returns false
               current_player_index = 1 - current_player_index  # Switch to next player's turn
       print(f"Game over... {self.players[current_player_index].player_name} wins!")  # Print winner