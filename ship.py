'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - ship.py
Purpose: Provides basic attributes and methods for Ship objects
Source(s):
https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich
'''
# This Ship class represents a ship object in the Battleship game.
# Code was modified from the original source to remove the "label" attribute and rename the class from "Boat" to "Ship".
class Ship:
   # Input: The size (length) of the ship
   # Output: A Ship object with attributes for size, position (x, y), and orientation (horizontal/vertical)
   # Description: Constructor for Ship objects. Initializes the ship with its size and default values for position and orientation.
   def __init__(self, size):
       self.size = size  # Size of the ship (1-5)
       self.x = None  # x-coordinate of the ship's position (column)
       self.y = None  # y-coordinate of the ship's position (row)
       self.orientation = None  # Ship's orientation (either 'horizontal' or 'vertical')
   # Input: Integers x and y representing the x-coordinate (column) and y-coordinate (row)
   # Output: None
   # Description: Set the "top left" position of the ship, which is used when placing the ship on the board.
   def set_position(self, x, y):
       self.x = x
       self.y = y
   # Input: A string representing the orientation of the ship ('horizontal' or 'vertical')
   # Output: None
   # Description: Sets the ship's orientation to either 'horizontal' or 'vertical', used when placing the ship on the board.
   def set_orientation(self, orientation):
       if orientation in ['horizontal', 'vertical']:
           self.orientation = orientation
       else:
           raise ValueError("Invalid orientation. Use 'horizontal' or 'vertical'.")