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
from game import Game

# Input: None
# Output: Displays game to players
# Description: create a Game object and start playing
# Written by Anakha Krishna and Isabel Loney
def main():
  game = Game()
  game.play()

# Entry Point
# Written by Isabel Loney
if __name__ == "__main__":
  main()