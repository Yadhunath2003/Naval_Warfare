'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - game.py
Purpose: Create and run battleship game
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich


Modified by Group 5
Modification start data: 9/25/2024
Modification end date: 9/29/2024
Modified by: Yadhunath Tharakeswaran
Changes made: Added the Computer feature to the game, so that the player has the flexibility to either play with the AI or Human.
The Computer player contains 3 levels of Difficulties: Easy, Medium, and Hard.
And they also have the ability to automatically place and attack the opponent's fleet automatically.
'''
# Code structure adapted from https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py BattleshipGame class and modified for this projects purposes
# Code written by Anakha Krishna
from player import Player
from ship import Ship
from ai import AIPlayer  # Import AIPlayer which now handles all difficulties

class Game:
    # Input: None
    # Output: A game object
    # Description: Game object constructor
    def __init__(self):
        self.fleet_options = {  # create lists of fleet types
            1: [Ship(1)],
            2: [Ship(1), Ship(2)],
            3: [Ship(1), Ship(2), Ship(3)],
            4: [Ship(1), Ship(2), Ship(3), Ship(4)],
            5: [Ship(1), Ship(2), Ship(3), Ship(4), Ship(5)]
        }
        self.fleet_type = None  # chosen fleet type 

    # Input: Player input specifying when to begin turn, where to place ships, and where to attack
    # Output: The player's own board and an opponent's board with ships hidden
    # Description: method to run the game, position boats, attack, and alternate turns until a player wins
    # The player 1 would be asked to play with an ai or human, and based on user's choice the game chooses the second player to be either ai or human.
    def play(self):
        print("Welcome to Battleship!")
        chosen_fleet = None
        while chosen_fleet is None:  # Prompt for fleet type until valid fleet type is given
            try:
                fleet_type = int(input("Choose how many ships will be in your fleet (1, 2, 3, 4, or 5): "))  # prompt user for fleet type
                if fleet_type in self.fleet_options:  # if valid input,
                    chosen_fleet = self.fleet_options[fleet_type]  # set fleet type in chosen_fleet for player 1 use
                    self.fleet_type = fleet_type
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Ask if the user wants to play against a computer or a human
        opponent_choice = input("Do you want to play against the computer or a human? (computer/human): ").strip().lower()
        chosen_fleet_copy = chosen_fleet.copy()  # Copy fleet for Player 2 (AI or human)
        
        if opponent_choice == "computer":
            # Ask for AI difficulty level
            difficulty = None
            while difficulty is None:
                try:
                    difficulty_input = int(input("Choose AI difficulty:\n1. Easy\n2. Medium\n3. Hard\nYour choice: "))
                    if difficulty_input in [1, 2, 3]:
                        if difficulty_input == 1:
                            difficulty = "Easy"
                        elif difficulty_input == 2:
                            difficulty = "Medium"
                        else:
                            difficulty = "Hard"
                    else:
                        print("Invalid choice. Please select 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            # Create human player, and Player 2 is the AI with chosen difficulty and board from Player 1
            player1 = Player("Player 1", chosen_fleet)
            ai_player = AIPlayer(difficulty, player1.board, chosen_fleet_copy)
            self.players = [player1, ai_player] ##The game is going to be ai vs human
            print(f"You will be playing against the computer ({difficulty} level).")

        else:
            # Both players are human players
            player1 = Player("Player 1", chosen_fleet)
            player2 = Player("Player 2", chosen_fleet_copy)
            self.players = [player1, player2]
            print("You will be playing against a human.")

        # Set opponent for each player
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

        # Player one places the fleet first
        self.players[0].place_fleet()

        # Depending on the choice they made, player 2 or ai will be placing thier fleet next.
        if isinstance(self.players[1], AIPlayer):
            self.players[1].place_ships()  # AI places ships automatically
        else:
            self.players[1].place_fleet()  # Human player manually places fleet

        input("All ships are placed. Press enter to begin the battle!")


        # Game loop
        game_over = False  # will handle take_turn() boolean result (True if game won, False if game continues)
        current_player_index = 0  # keeps track of whose turn it is, starting with Player 1

        while not game_over:
            current_player = self.players[current_player_index]  # Start with Player 1 or AI/Human opponent

        # If the current player is Player 1 (Human), ask for input to take a turn
            if current_player_index == 0 and isinstance(current_player, Player):
                game_over = current_player.take_turn(self.fleet_type)  # Human player takes turn
            else:
                # If the current player is the AI, automatically take its turn
                if isinstance(current_player, AIPlayer):
                    print(f"{current_player.player_name}'s turn (AI - {current_player.difficulty})...")
                else:
                    print(f"{current_player.player_name}'s turn (Human)...")

                # AI or second human player takes turn
                game_over = current_player.take_turn(self.fleet_type)

            # Switch turns if the game is not over
            if not game_over:
                current_player_index = 1 - current_player_index  # Switch between Player 1 and Player 2 (AI or Human)

        # Game over: announce the winner
        if isinstance(self.players[current_player_index], AIPlayer):
            print("Game over... AI wins!")
        else:
            print(f"Game over... {self.players[current_player_index].player_name} wins!")