from game_logic import GameBoard
from player import Player
import random

class GamePlay:
    def __init__(self, player1, player2, mode="PvP"):
        """
        Initialize the gameplay logic.
        mode: "PvP" for Player vs. Player, "PvAI" for Player vs. AI.
        """
        self.player1 = player1
        self.player2 = player2
        self.mode = mode
        self.current_player = player1
        self.opponent = player2
        self.winner = None
        self.game_over = False
        self.turns = 0  # Track the total number of turns
        self.player1_turns = 0  # Track Player 1's turns
        self.player2_turns = 0  # Track Player 2's turns

    def attack(self, x, y):
        """
        Handle an attack on the opponent's board and update the current player's attack grid.
        """
        # Check if the position has already been attacked on the opponent's board
        if self.opponent.board.is_attacked(x, y):
            return {"valid": False, "message": "Cell already attacked. Try again."}

        # Record the attack on the opponent's board
        self.opponent.board.mark_attacked(x, y)

        if self.opponent.board.grid[y][x] == 'S':  # Hit
            self.opponent.board.grid[y][x] = 'X'  # Mark hit on the opponent's grid
            self.current_player.board.update_attack_grid(x, y, True)  # Update attack_grid
            self.current_player.hits.append((x, y))  # Track hit
            return {"valid": True, "hit": True, "message": "Hit!"}

        elif self.opponent.board.grid[y][x] == '-':  # Miss
            self.opponent.board.grid[y][x] = 'O'  # Mark miss on the opponent's grid
            self.current_player.board.update_attack_grid(x, y, False)  # Update attack_grid
            self.current_player.misses.append((x, y))  # Track miss
            return {"valid": True, "hit": False, "message": "Miss!"}

    def random_attack(self, opponent_board):
        """
        Randomly select an unplayed cell on the opponent's board for an attack.
        """
        available_moves = [
            (x, y) for x in range(self.cols)
                    for y in range(self.rows)
                    if not opponent_board.is_attacked(x, y)
        ]
        if not available_moves:
            return None, None  # No available moves
        return random.choice(available_moves)

    def check_victory(self):
        """
        Check if the opponent has lost all their ships.
        """
        for row in self.opponent.board.grid:
            if 'S' in row:  # Check if any ships remain
                return False
        self.winner = self.current_player.name
        self.game_over = True
        return True

    def switch_turns(self):
        """
        Switch the current player and opponent.
        """
        self.current_player, self.opponent = self.opponent, self.current_player

    def process_turn(self, x=None, y=None):
        """
        Process the current player's turn.
        For AI, make a move automatically.
        """
        if self.mode == "PvAI" and self.current_player == self.player2:
            # AI's turn
            x, y = self.current_player.board.random_attack(self.opponent.board)

        # Validate the move coordinates
        if x is None or y is None:
            return {"valid": False, "message": "Invalid coordinates.", "hit": False}

        # Perform the attack
        attack_result = self.attack(x, y)
        if not attack_result["valid"]:
            # Ensure "hit" key is included in the response
            return {"valid": False, "message": attack_result["message"], "hit": False}

        # Add "hit" to the result if it's not already there
        attack_result["hit"] = attack_result.get("hit", False)

        # Display the updated game state
        self.display_game_state()

        # Check if the game is over
        if self.check_victory():
            return {"valid": True, "winner": self.winner, "message": f"{self.winner} wins!", "hit": attack_result["hit"]}

        # Increment total and player-specific turn counters
        self.turns += 1
        if self.current_player == self.player1:
            self.player1_turns += 1
        else:
            self.player2_turns += 1

        # Switch turns if the game isn't over
        self.switch_turns()
        return attack_result


    
    def display_game_state(self):
        """
        Print the current state of the game to the terminal.
        """
        print(f"\n{self.current_player.name}'s Turn:")
        print("Your Board:")
        for row in self.current_player.board.grid:
            print(" ".join(row))
        print("\nOpponent's Board (Your Attacks):")
        for row in self.current_player.board.attack_grid:
            print(" ".join(row))
        print("\n")

    def reset_game(self):
        """
        Reset the game state for a new match.
        """
        self.current_player = self.player1
        self.opponent = self.player2
        self.winner = None
        self.game_over = False
        self.player1.board = GameBoard()
        self.player2.board = GameBoard()


        