"""
File Name: ai.py
Date Created: 23 September 2024
Date Completed: 28 September 2024
Created By: Sanketh (Medium), Kemar (Easy, Hard)
Tested By: Yadhunath
Status: Everything is Working Well!
"""

import random
from player import Player
from board import Board

class AIPlayer(Player):
    def __init__(self, difficulty, player_name, fleet):
        # Initialize the AI player with a given difficulty level, the game board, and a fleet of ships.
        super().__init__(player_name, fleet)
        self.difficulty = difficulty
        self.last_hit = None  # Tracks the last successful hit to focus on targeted firing
        self.previous_hits = []  # List to track all the successful hits, useful for more advanced strategies
        
        # Creates a list of all possible moves (coordinates) on the board, then shuffle it create randomness
        self.possible_moves = []
        for x in range(10):
            for y in range(10):
                self.possible_moves.append((x, y))  # Generates all coordinates (x, y) on the 10x10 board
        random.shuffle(self.possible_moves)  # Shuffles for randomization of AI moves
        
        self.adjacent_moves = []  # List to store the moves adjacent to a hit, used for targeted firing

    def place_ships(self):
        """
        Automatically places the ships for AI on the board.
        Randomly generates the position and orientation for each ship and places them.
        """
        for ship in self.fleet:
            placed = False
            while not placed:
                # Randomly chooses between horizontal or vertical orientation for the ship
                orientation = random.choice(['horizontal', 'vertical'])

                # Generates random starting positions based on the ship's orientation and size
                if orientation == 'horizontal':
                    x = random.randint(0, 10 - ship.size)  # Ensures that the ship fits horizontally
                    y = random.randint(0, 9)  # Random row position
                else:
                    x = random.randint(0, 9)  # Random column position
                    y = random.randint(0, 10 - ship.size)  # Ensures that the ship fits vertically

                # Sets the ship's position and orientation
                ship.set_position(x, y)
                ship.set_orientation(orientation)

                # Attempts to place the ship on the board, ensuring no overlap with other ships
                placed = self.board.place_ship(ship)
        
        print(f"{self.player_name} has placed all ships.")  # Notifies that the ship placement is complete

    def fire(self):
        """
        Decides where the AI will fire based on its difficulty level.
        Different strategies are used depending on whether it's 'Easy', 'Medium', or 'Hard'.
        """
        if self.difficulty == 'Easy':
            return self.fire_random()  # Easy mode: purely random firing
        elif self.difficulty == 'Medium':
            if self.last_hit:
                return self.fire_near_last_hit()  # Medium mode: targeted firing after a hit
            else:
                return self.fire_random()  # If no previous hit, revert to random firing
        elif self.difficulty == 'Hard':
            return self.cheat_fire()  # Hard mode: AI cheats and knows the location of ships

    def fire_random(self):
        """
        Fires at a random location chosen from the list of possible moves.
        """
        move = self.possible_moves.pop()  # Pop removes and returns the last move from the shuffled list
        print(f"{self.player_name} fires at random location {move}.")
        return move

    def fire_near_last_hit(self):
        """
        Fires at a location adjacent to the last successful hit, used in Medium difficulty.
        """
        if not self.adjacent_moves:  # If no adjacent moves are queued up, find them
            self.adjacent_moves = self.get_adjacent(self.last_hit[0], self.last_hit[1])
        if self.adjacent_moves:  # If there are adjacent moves available
            move = self.adjacent_moves.pop()  # Choose one of the adjacent moves
            print(f"{self.player_name} fires near last hit at {move}.")
            return move
        else:
            return self.fire_random()  # If no adjacent moves are possible, revert to random firing

    def cheat_fire(self):
        """
        In Hard mode, the AI cheats by knowing exactly where the opponent's ships are.
        This method scans the opponent's board for any ship and fires directly at it.
        """
        for x in range(10):
            for y in range(10):
                if self.opponent.board.grid[y][x] == ' S':  # Checks for ship ('S') on the opponent's board
                    print(f"{self.player_name} cheats and fires at location ({x+1}, {y+1})!")
                    return x, y  # Returns the exact position of the opponent's ship

    def get_adjacent(self, x, y):
        """
        Finds and returns a list of valid adjacent positions to the given (x, y) coordinate.
        This helps the AI focus on areas near a hit.
        """
        options = [
            (x + 1, y),  # Right
            (x - 1, y),  # Left
            (x, y + 1),  # Down
            (x, y - 1)   # Up
        ]
        random.shuffle(options)  # Shuffles the options to add randomness to the adjacent targeting
        
        # Filter's out the positions that are out of bounds or already attacked
        for new_x, new_y in options:
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.opponent.board.grid[new_y][new_x] not in [' X', ' O']:
                return [(new_x, new_y)]  # Returns a list of valid adjacent positions
        return []

    # Take turn function adapted from player.py to execute the AI's turn automatically
    def take_turn(self, fleet_type):
        """
        Executes the AI's turn, determining a firing position and attacking the opponent.
        """
        move = self.fire()  # Get the firing position based on the AI's difficulty strategy
        if self.opponent.board.attack(*move):
            print(f"{self.player_name} hits at {move}!")
            self.hits += 1  # Update hits
            self.last_hit = move
        else:
            print(f"{self.player_name} misses at {move}.")
            self.misses += 1  # Update misses
        # Display the board after the AI takes a turn
        print("Opponent's board after AI turn:")
        print(self.opponent.board.opponent_view())
        return self.opponent.board.defeat(fleet_type)