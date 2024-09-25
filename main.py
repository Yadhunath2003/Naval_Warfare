'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - game.py
Purpose: Entry point for running the battleship game. Creates the game and begins it
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py for overall program structure 
Other collaborators: Code reviewed and tested by Jackson Wunderlich, modified by Isabel Loney
'''
from player import Player
from ai_player import AIPlayer
from game import Game
from ship import Ship
def main():
   print("Welcome to Battleship!")
   # Initialize player 1
   player1_name = input("Enter Player 1's name: ")
   player1_fleet = [Ship(5), Ship(4), Ship(3), Ship(3), Ship(2)]
   player1 = Player(player1_name, player1_fleet)
   # Ask if Player 2 is human or AI
   opponent_choice = input("Do you want to play against a human or AI? (human/AI): ").strip().lower()
   if opponent_choice == "ai":
       difficulty = input("Select AI difficulty (Easy/Medium/Hard): ").strip().capitalize()
       player2_fleet = [Ship(5), Ship(4), Ship(3), Ship(3), Ship(2)]
       player2 = AIPlayer(difficulty, player1.board, player2_fleet)
   else:
       player2_name = input("Enter Player 2's name: ")
       player2_fleet = [Ship(5), Ship(4), Ship(3), Ship(3), Ship(2)]
       player2 = Player(player2_name, player2_fleet)
   # Set opponents
   player1.set_opponent(player2)
   player2.set_opponent(player1)
   # Create and start the game
   game = Game(player1, player2)
   game.play()
if __name__ == "__main__":
   main()