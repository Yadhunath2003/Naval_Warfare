'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - game.py
Purpose: Create and run battleship game
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich
Modified by Group 5: Added the Computer feature to the game
'''

from player import Player
from ship import Ship
from ai import AIPlayer  # Import AIPlayer which now handles all difficulties

class Game:
    def __init__(self):
        self.fleet_options = {
            1: [Ship(1)],
            2: [Ship(1), Ship(2)],
            3: [Ship(1), Ship(2), Ship(3)],
            4: [Ship(1), Ship(2), Ship(3), Ship(4)],
            5: [Ship(1), Ship(2), Ship(3), Ship(4), Ship(5)]
        }
        self.fleet_type = None

    def play(self):
        print("Welcome to Battleship!")
        chosen_fleet = None
        while chosen_fleet is None:
            try:
                fleet_type = int(input("Choose how many ships will be in your fleet (1, 2, 3, 4, or 5): "))
                if fleet_type in self.fleet_options:
                    chosen_fleet = self.fleet_options[fleet_type]
                    self.fleet_type = fleet_type
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        opponent_choice = input("Do you want to play against the computer or a human? (computer/human): ").strip().lower()
        chosen_fleet_copy = chosen_fleet.copy()

        if opponent_choice == "computer":
            difficulty = None
            while difficulty is None:
                try:
                    difficulty_input = int(input("Choose AI difficulty:\n1. Easy\n2. Medium\n3. Hard\nYour choice: "))
                    if difficulty_input in [1, 2, 3]:
                        difficulty = ["Easy", "Medium", "Hard"][difficulty_input - 1]
                    else:
                        print("Invalid choice. Please select 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            player1 = Player("Player 1", chosen_fleet)
            ai_player = AIPlayer(difficulty, f"Computer ({difficulty})", chosen_fleet_copy)
            self.players = [player1, ai_player]
            print(f"You will be playing against the computer ({difficulty} level).")
        else:
            player1 = Player("Player 1", chosen_fleet)
            player2 = Player("Player 2", chosen_fleet_copy)
            self.players = [player1, player2]
            print("You will be playing against a human.")

        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

        self.players[0].place_fleet()

        if isinstance(self.players[1], AIPlayer):
            self.players[1].place_ships()
        else:
            self.players[1].place_fleet()

        input("All ships are placed. Press enter to begin the battle!")

        game_over = False
        current_player_index = 0

        while not game_over:
            current_player = self.players[current_player_index]

            if current_player_index == 0 and isinstance(current_player, Player):
                game_over = current_player.take_turn(self.fleet_type)
            else:
                if isinstance(current_player, AIPlayer):
                    print(f"{current_player.player_name}'s turn (AI - {current_player.difficulty})...")
                else:
                    print(f"{current_player.player_name}'s turn (Human)...")
                game_over = current_player.take_turn(self.fleet_type)

            # Call display_scorecard after each player's turn
            self.display_scorecard()

            if not game_over:
                current_player_index = 1 - current_player_index

        # Game over: announce the winner and display the final scorecard
        if isinstance(self.players[current_player_index], AIPlayer):
            print("Game over... AI wins!")
        else:
            print(f"Game over... {self.players[current_player_index].player_name} wins!\n")

        # Final display of the scorecard after the game ends
        self.display_scorecard()

    def display_scorecard(self):
        print(f"Scorecard:")
        for player in self.players:
            print(f"\n{player.player_name}: Hits - {player.hits}, Misses - {player.misses}\n")
