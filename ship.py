'''
Author: Anakha Krishna
Creation Date: 
Last Modified: 
Commenting: All comments written on 
Program Name: 
Purpose:
Source(s): 
'''

class Ship:
    # Input: the size (length) of the ship
    # Output: A ship object
    # Description: Ship object constructor
    def __init__(self, size):
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None

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
