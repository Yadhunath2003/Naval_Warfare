'''
Author: Anakha Krishna
Creation Date: 9/10/24
Last Modified: 9/15/24
Commenting: All comments written on 9/15/24 by Anakha Krishna and Isabel Loney
Program Name: Battleship - ship.py
Purpose: Provides basic attributes and methods for Ship objects
Source(s): https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py
Other collaborators: Code reviewed and tested by Jackson Wunderlich
'''
# All code in this file is from https://ils.unc.edu/courses/2017_spring/inls560_001/a/battleship.py Boat class.
# Code was modified to not include "label" attribute and be renamed as "Ship" instead of "Boat"
class Ship:
    # Input: the size (length) of the ship
    # Output: A ship object
    # Description: Ship object constructor
    def __init__(self, size):
        self.size = size # size of ship (1-5)
        self.x = None # x coordinate of ship position
        self.y = None # y coordinate of ship position
        self.orientation = None # ship orientation (to be vertical or horizontal)

    # Input: Integers x and y representing x-coordinate (column) and y-coordinate (row)
    # Output: None
    # Description: Set the "top left" position of the ship, used by place_ship functions
    def set_position(self, x, y):
        self.x = x
        self.y = y

    # Input: orientation as string, all lowercase: 'horizontal' or 'vertical'
    # Output: None
    # Description: Set orientation of ship as vertical or horizontal, used by place_ship functions
    def set_orientation(self, orientation):
        self.orientation = orientation
